---
source: rss/assetnote-blog
title: Leaking File Contents with a Blind File Oracle in Flarum
url: https://blog.assetnote.io/2023/08/28/leaking-file-contents-with-a-blind-file-oracle-in-flarum/
date: 2023-08-27
item_id: https://blog.assetnote.io/2023/08/28/leaking-file-contents-with-a-blind-file-oracle-in-flarum/
category: techniques
tags: [CVE, Idor, Ssrf]
---

**Source:** Assetnote Blog
**Link:** https://blog.assetnote.io/2023/08/28/leaking-file-contents-with-a-blind-file-oracle-in-flarum/

Introduction 

 Flarum is a free, open source PHP-based forum software used for everything from gaming hobbyist sites to cryptocurrency discussion. A quick survey on Shodan suggests there are over 1200 installs exposed to the internet. 

 Through our research we were able to leak the contents of arbitrary local files in Flarum through a blind oracle, and conduct blind SSRF attacks with only a basic user account. 

  We continue to perform original security research in an effort to alert our customers to zero-day vulnerabilities in their attack surface. As users of our  Attack Surface Management  platform, our customers are the first to know when they are affected by new vulnerabilities.  

 Understanding the Flarum Software 

 Since Flarum is open source software, there was no need for reverse engineering. We quickly realised that the vast majority of code for a Flarum installation comes from the  flarum/framework  repository, which is available  on Github . The first step in analysing the application was to figure out which routes were accessible. Unlike many other software applications we assess at Assetnote, due to Flarum’s nature as forum software, the majority of installations typically permit users to create their own accounts. This means that authenticated routes are also interesting, as long as they don’t require administrative permissions. 

 We quickly figured out that files called  routes.php  in different directories provided routing for most of the application, and in particular that  framework/core/src/Api/routes.php  listed a lot of interesting routes: 

  
use Flarum\Api\Controller;
use Flarum\Http\RouteCollection;
use Flarum\Http\RouteHandlerFactory;

return function (RouteCollection $map, RouteHandlerFactory $route) {
    // Get forum information
    $map-&gt;get(
        '/',
        'forum.show',
        $route-&gt;toController(Controller\ShowForumController::class)
    );

    ... 

    // Send test mail post
    $map-&gt;post(
        '/mail/test',
        'mailTest',
        $route-&gt;toController(Controller\SendTestMailController::class)
    );
};
  

 We quickly ruled out a lot of otherwise interesting routes that required admin permissions, such as  /mail/test . After a while of looking through the code route by route, we identified a potentially interesting API endpoint that allowed users to update their forum avatar: 

  // Upload avatar
$map-&gt;post(
    '/users/{id}/avatar',
    'users.avatar.upload',
    $route-&gt;toController(Controller\UploadAvatarController::class)
);
  

 We then dived into the  UploadAvatarController  for a closer look. 

 Looking at the Upload Functionality 

 The code of the  UploadAvatarController  is very straightforward: 

  protected function data(ServerRequestInterface $request, Document $document)
{
    $id = Arr::get($request-&gt;getQueryParams(), 'id');
    $actor = RequestUtil::getActor($request);
    $file = Arr::get($request-&gt;getUploadedFiles(), 'avatar');

    return $this-&gt;bus-&gt;dispatch(
        new UploadAvatar($id, $file, $actor)
    );
}
  

 The route takes a user  id  in the query parameter, and a file upload named  avatar , and dispatches an  UploadAvatar  action to the bus. This is then handled in the  UploadAvatarHandler  class in  framework/core/src/User/Command/UploadAvatarHandler.php : 

  class UploadAvatarHandler
{
    use DispatchEventsTrait;

    ...

    /**
     * @var ImageManager
     */
    protected $imageManager;

    ...

    public function handle(UploadAvatar $command)
    {
        $actor = $command-&gt;actor;

        $user = $this-&gt;users-&gt;findOrFail($command-&gt;userId);

        if ($actor-&gt;id !== $user-&gt;id) {
            $actor-&gt;assertCan('edit', $user);
        }

        $this-&gt;validator-&gt;assertValid(['avatar' =&gt; $command-&gt;file]);

        $image = $this-&gt;imageManager-&gt;make($command-&gt;file-&gt;getStream());

        $this-&gt;events-&gt;dispatch(
            new AvatarSaving($user, $actor, $image)
        );

        $this-&gt;uploader-&gt;upload($user, $image);

        $user-&gt;save();

        $this-&gt;dispatchEventsFor($user, $actor);

        return $user;
    }
}
  

 Here the function checks we have access to change the avatar of the user with that ID, which prevents a trivial IDOR. However, we are more interested in the behavior of the  imageManager-&gt;make  function. The  ImageManager  is sourced from the Intervention Image library. What is that? 

 When Library Code is Dangerous by Default 

 Intervention Image  is a PHP image handling and manipulation library  that provides a simple interface to load, store, and edit images. Let’s start by looking at the documentation for the  ImageManager ’s  make  method: 

  Universal factory method to create a new image instance from source. The method is highly variable to read all the input types listed below.
  

 The library then lists a bunch of methods you can use to supply an image: 

      string - Path of the image in filesystem.
    string - URL of an image (allow_url_fopen must be enabled).
    string - Binary image data.
    string - Data-URL encoded image data.
    string - Base64 encoded image data.
    resource - PHP resource of type gd. (when using GD driver)
    object - Imagick instance (when using Imagick driver)
    object - Intervention\Image\Image instance
    object - SplFileInfo instance (To handle Laravel file uploads via Symfony\Component\HttpFoundation\File\UploadedFile)
  

 This immediately raises alarm bells. We are providing a string to this method (not exactly, but an object with a  __toString()  magic method) and have full control. In the happy path, this just ‘works’ since one of the options is binary image data. But what happens if we upload a file containing a URL? 

 To understand the impact, let’s dive into the sources of the image library: 

  namespace Intervention\Image;

abstract class AbstractDecoder
{
    // ...

    public function init($data)
    {
        $this-&gt;data = $data;

        switch (true) {

            case $this-&gt;isGdResource():
                return $this-&gt;initFromGdResource($this-&gt;data);

            case $this-&gt;isImagick():
                return $this-&gt;initFromImagick($this-&gt;data);

            case $this-&gt;isInterventionImage():
                return $this-&gt;initFromInterventionImage($this-&gt;data);

            case $this-&gt;isSplFileInfo():
                return $this-&gt;initFromPath($this-&gt;data-&gt;getRealPath());

            case $this-&gt;isBinary():
                return $this-&gt;initFromBinary($this-&gt;data);

            case $this-&gt;isUrl():
                return $this-&gt;initFromUrl($this-&gt;data);

            case $this-&gt;isStream():
                return $this-&gt;initFromStream($this-&gt;data);

            case $this-&gt;isDataUrl():
                return $this-&gt;initFromBinary($this-&gt;decodeDataUrl($this-&gt;data));

            case $this-&gt;isFilePath():
                return $this-&gt;initFromPath($this-&gt;data);

            // isBase64 has to be after isFilePath to prevent false positives
            case $this-&gt;isBase64():
                return $this-&gt;initFromBinary(base64_decode($this-&gt;data));

            default:
                throw new NotReadableException("Image source not readable");
        }
    }
}
  

 We are interested in particular in the functionality when the string supplied is a URL, so let’s see what checks are done: 

      public function isUrl()
    {
        return (bool) filter_var($this-&gt;data, FILTER_VALIDATE_URL);
    }

    // ...

    public function initFromUrl($url)
    {
        
        $options = [
            'http' =&gt; [
                'method'=&gt;"GET",
                'protocol_version'=&gt;1.1, // force use HTTP 1.1 for service mesh environment with envoy
                'header'=&gt;"Accept-language: en\r\n".
                "User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36\r\n"
          ]
        ];
        
        $context  = stream_context_create($options);
        

        if ($data = @file_get_contents($url, false, $context)) {
            return $this-&gt;initFromBinary($data);
        }

        throw new NotReadableException(
            "Unable to init from given url (".$url.")."
        );
    }
  

 Our user input gets passed into  file_get_contents  without any validation, except that it must ‘look like’ a URL! This is known to be incredibly dangerous. The one limitation is that the content to leak must be a valid image, otherwise an error is thrown when the library parses the contents. We can start to brainstorm ways we can abuse this functionality: 

 
   We could pass an internal URL such as  http://localhost:8100/favicon.ico , and possibly leak that image if it exists. 
   We could pass an internal URL such as  http://localhost:9001/do/evil/action?param=foo , and conduct a blind SSRF attack. 
   More worryingly, despite the stream context, PHP is happy to accept a  file  URI, so an input like  file:///home/foo/secret.png  could possibly reveal the contents of an image on the local filesystem. 
 

 While these definitely are vulnerabilities, they are context-dependent and are not so impactful. Can we do better? It turns out, using blind file oracle, we can! 

 Blind File Oracles 101 

 First revealed in the DownUnderCTF 2022, there is a technique for leaking the contents of arbitrary files using the  php://  wrapper even if the output of the file read is not given to the user. In our case, the files we want to read are most likely not going to form valid images, so this is a perfect application of this technique. In summary, this attack hinges on two features of the  php://filter  wrapper. 

 The first is that the filter wrapper supports converting between two different charsets using the  convert.iconv  function. For instance, the request  php://filter/convert.iconv.latin1.UTF-32/resource=/etc/passwd  would take the contents of  /etc/passwd  and convert it from the latin1 charset to UTF-32. In this case, the file content gets mapped to something like this: 

  latin1: root:x: 
UTF-32: r\0\0\0o\0\0\0o\0\0\0t\0\0\0:\0\0\0x\0\0\0:\0\0\0
  

 Note how the output blows up 4x in size, because each latin1 char is encoded in a fixed 4 bytes of UTF-32. If we repeat this process, the string will blow up to 16x, 64x, 256x size, and so on, and eventually the string will grow so large it will exceed the memory limit and cause the PHP process to stop and return 500. However, if the file we point to is empty or does not exist, no 500 error will be generated. This forms an oracle we can use to test for emptiness. 

 On its own this is not so useful, but PHP has another interesting ‘feature’ - the  dechunk  filter. The  dechunk  filter was intended for parsing HTTP chunks, but its behavior on arbitrary strings are as follows: 

 
   If the string is a single line and begins with one of  0-9a-fA-F , the whole line is removed; 
   Otherwise, the string remains untouched. 
 

 We can now leak information from a file as follows: 

 
   Base64 encode the file using the  convert.base64-encode  function; 
   Apply the dechunk filter; 
   Blow up the string multiple times using a latin1 - UTF32 conversion. 
 

 If we don’t get a 500, we know that the file contents in base64 must have started with one of  0-9a-fA-F . Otherwise, if we do get a 500, we know it can’t have started with those characters (so it must be in  g-zG-Z+/ ) 

 The full file leak is more complicated and uses multiple iconv conversions to swap other characters to the front and precisely determine which character is at the front. The gory details are explained in the original challenge’s  solution script  and in a  blog post written by Synacktiv . 

 Summarising, with a simple modification to the above script we are able to use the technique to leak the contents of any file on the server. 

 Remediation 

 Flarum fixed this vulnerability promptly and versions  &gt;= 1.8.0  are no longer vulnerable. Their advisory is available  here . The vulnerability was assigned CVE-2023-40033. 

 We have tried reaching out to the developers of  Intervention/Image  several times with some suggestions to make the library less vulnerable by default, but have got no response. If you are using this library, the best way to ensure you are not vulnerable is by never passing user data directly into the constructor; if you are wanting to turn an upload into an image, pass the file path to the uploaded tempfile instead. 

 Conclusion 

 In this blog post, we have seen that a small error in how a library for image manipulation was used resulted in the ability to leak the contents of any file on disk. We have also shown that the PHP blind file oracle which originated in a CTF challenge has real-world applicability and should be kept in mind when auditing PHP source code. 

 As always, customers of our Attack Surface Management platform were the first to know when this vulnerability affected them. We continue to perform original security research in an effort to inform our customers about zero-day vulnerabilities in their attack surface.
