# Why this repo exists?
This repo inherit the previous boiler plate from the engine i made, 
but this repo will be more focus on creating the ocean surface through a more emprical, statistical approach
when combining large ammount of oscillating functions together, aiming for the nearest replication of the Tessendorf paper
# Limitation
Although me, myself, has been keeping an eye on the paper for more than a whole year. 
Despite that, limitations. For examples, a huge gap in expertise, knowledge and experience 
has been gatekeeping from ever understand some of the sections featured in the paper.
This part will listing all the caveats of my wave surface implementation, in comparision with the model featured in the paper:
    - No FFT
    - No realistic PBR (only consist of Fresnel, no regard to the ocean radiosity model)
    - no Choppy waves - the choppy waves formula represented in the paper is belong to the "Fourier domain", 
    of which i'm incapable of understanding the concept. 
    Yes, i can roll my own implementation to simulating, trying to replicate the choppiness, 
    but it would be really time-inefficient as it would be a trial and error process. 
    Moreover, at the moment, i'm way more enthusiastic in filling up the gap in my maths knowledge, and learning more advanced OpenGL rendering features.
    Hence, i would leave it to myself in the future, by the time i finish the Fourier analysis thingy
# Conclusion
I don't know shit