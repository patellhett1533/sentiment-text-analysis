from deepface import DeepFace

img_info = DeepFace.analyze("images/het.jpeg")
prompt = "generate an headshot image for linkedin profile picture with a professional dress and hair style with small smile"

generated_image = generate_image_based_on_prompt(prompt, img_info)
print(generated_image)
