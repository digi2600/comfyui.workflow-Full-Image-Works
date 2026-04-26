I have created a very large and, I think very unique workflow that is very advanced, but I am afraid it is advanced in some areas and missing some of the more basic parts. I have been making it by trial and error as I go along, and have made it really flexible. There are two main sections or Steps. First is the input step. A long side of the workflow with dynamic choices for text-to-image, image-based + text-to-image, inpainting, photo restoration, flux-only, and a few more. The second step is the fine-tuning part. Again, fully dynamic, where you can pick and/or all of the "modules" like skin fix, face fix, K-Sampler Cycle fix, face swap, upscale, and more.
Some parts have been added and adapted from other sources on the internet. An example is the flux image generation part. I did not make that one, but I did use other nodes to incorporate it into the workflow as another generation option within the list of "step 1" generation choices.
There are options within options here that are constantly being rewritten, streamlined, and even a few unfinished parts. I'll try to keep this as short as possible while hopefully explaining a good amount.

Heads up: I have created this using a Windows box with an AMD 16GB VRAM card. It has taken me months to find the perfect balance of torch/Rocm/nodes/drivers and more. Due to possible health and family concerns, I am trying to add this to a public repo asap and have not written everything down yet. This will take a number of custom nodes that I think many people will have problems with, and it might not be the most efficient, but it is working for me, and I have only been using ComfyUI image generation for about 9 months now.

Step 1:
First, start by selecting one of several different ways to start within the "Step 1" section.
-Generate Image from Text. By default, it will create a batch of 4 images.
  You have the "set" box where you can choose :
    *the checkpoint, steps, cfg, and other normal settings, including the width and height. 
    *batch size should stay at 4, but I think 2 is doable, but not very tested.
    *Vram usage is selectable from 1 (full VAE decode) and 2 (tiled decode, using less Vram.)
    *stop_at_clip_layer option to control clip encoding for lesser or greater detail/control.
    **Vram debugging and clearing to increase speed and effecentcy.
  The power lora loader by rgthree to load any lora's you wish.
  The rgthree seed selector node makes seed control much easier and faster.
  Main positive prompt and Negative prompt.
  2nd positive prompt using Prompt database from benstaniford/comfy-prompt-db, to enable a quick selection of normally used prompts. This can be used in addition to the first positive prompt, the only positive prompt, or just left blank. It's all dynamic.
  The preview image box should show each image generated in the batch, and is always the best way to save any image you choose.


  !!Once you generate a good image that you like, select little the box next to the end that says "Batch image" and shows "Image #" as this will send only the image from the batch that you like to "step 2"-image adjustment.
  
-Generate Image from Image and Text. By default, it will create a batch of 4 images. 
You have the "set" box where you can choose :
    *the checkpoint, steps, cfg, and other normal settings, including the width and height. (Remember to mess with denoise to give the  generating model more or less freedom in the new image!)
    *fit should be ‘contain’ in most cases.
    *amount is the amount in batch to generate. 4 is the best as I have found.
The power lora loader by rgthree to load any lora's you wish.
  The rgthree seed selector node makes seed control much easier and faster.
Main positive prompt and Negative prompt.
Image Comparer (rgthree) allowing you to compare each image in the batch to the original image.
The preview image box should show each image generated in the batch, and is always the best way to save any image you choose.
Note 1: While this has the same looking “Batch Image” select box at the end of the section like above, it is not updated to the same number scheme yet. For image 1, select 0. For image 2 select 1, and so on.
Note 2: This only uses the more efficient tile VAE decode



-Inpaint. Can be tricky. The end of the section has a second model selected to go off a non-Inpaint model.

-Flux. Use text to image generation with Fulx.

-Image to text. Reads images into text descriptions. See how an AI describes images. You can also take the description and copy it to the 'Generate Image from Text' to change it any way you want.

-Restore Image

-Florance2 image to text. Another type of image to text nodes that usually gives better or more detailed results.

(Note: Press the number 1 to jump back to step 1, choosing area.)


Step 2:
You can choose to enable any option, or options, to continue. This was added to make it easier to generate several times until you get a result you want to work with.

-Fine Tune Image
Will take the one image you selected from the previous batch of pictures and give it a re-touch. A light re-draw to the full image to help with artifacts or changes. This will give you a new batch of 4 images (same "Batch image" and shows "Image #" as above).

-Skin Fix
It is usually best to do this step before a Face or Hand Fix. Remember: Each 'Fix' has positive and negative prompts for each section.

-Face Fix
Regenerate a new face. Many faces you generate will have bad faces, like crooked eyes, or something wrong, but the body is perfect. This will help if you used too many loras and messed up the face.

-Hand Fix
This will try to find and fix broken or messed-up fingers and hands.

-Ksampler Cycle Fix
Much like 'Fine Tune Image', this will redraw the image using cycles of the sampler and combine them. This is more focused on blending and refining any 'Fix', but can be used alone, without any other 'Fix' enabled.

-Face Swap
Use face swap to change the face on the image to another face. (Up to four different face swaps per image!)

-Face Swap (SimSwap)
A different version of Face Swap is used. SimSwap is a higher-quality and more adjustable tool, but it is also very hard to get right.

-Blend and Adjust Face Expression
Change the lighting, contrast, and other image settings with the ability to change some facial parameters.
 
-Upscale
1x and 2x Upscale with a second preview window showing the 1x upscale version without the enlargement at full 1 to 1 quality. Upscales will have some light image enhancement and fine detail added(like hair, face, etc.).

-Test video creation node

Just click any yes or no button(s) in the Choose menu step 2. All Choice Groups are fully modular and made to work in any combination or number, but they can not change the direction (i.e., no Upscale before Face Swap. Only Face Swap and then Upscale.) So you can use the Face Fix and the Upscale while leaving Fine Tune, Face Swap, and Blend and Adjust Face Expression disabled, and it should just skip them. But I suggest only activating extra groups one at a time (You don't have to process more until you are ready, otherwise it will be a lot of wasted generations and slow things down. A good example is if I wanted to do Face Fix and Upscale, I would first do Face Fix, then come back to this menu (press '2' to jump here) and then enable Upscale, leaving Face Fix still on.)

Would I ever do Face Fix and Face Swap at once? Well, yes. I have had several face swaps that looked odd because the face finder didn't work well and gave her a crooked jaw or no real lower lip...so A fresh regen of the face might help.
Remember: Face Fix (Or regen) will capture ANY face (Picture on a shirt, poster, background guy, anything. But the Face Swap only works on one face unless you mess with the input_faces_index, and there is no way to get the Expressions node to work with more than one face, so you might find it useful to do a face regen on a photo of two hikers when they find a bear. Use Face Fix to tweak the facial features just about right, then do a face swap, and the face swap should overlay the face on top, not overwrite it. But just in case...now you can. Yay!

(Note: Press the number 2 to jump back to this area to enable different things!)

******************************************

Python version: 3.11.9

AMD arch: gfx1201
ROCm version: (7, 2)

ComfyUI version: 0.11.1
ComfyUI frontend version: 1.37.11

Torch version: 2.10.0+rocm7.12.0a20260201



