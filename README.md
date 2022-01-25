# Lip-Reader

This project is a simple web-based app that performs visual lip reading using Hahn orthogonal moments for feature extraction  

In this version, we use Python 3.9, PyTorch 1.9.0 and dlib 19.22.1


## Install Libraries

```bash
pip install requirements.txt
```

## Install FFmpeg

**For MacOS**

Once you have Homebrew installed install ffmpeg from the terminal with the following:
```bash
brew install ffmpeg
```

**For Windows**

<a href="https://www.thewindowsclub.com/how-to-install-ffmpeg-on-windows-10" target="_blank"><i>Install FFmpeg on Windows</i></a>

**For Linux**
```bash
sudo apt install ffmpeg
```

## Download Facial Landmark Shape Predictor
**Using Kaggle**
```bash
kaggle datasets download -d codebreaker619/face-landmark-shape-predictor
```
Copy file to `lip-reading-service/src/ALR/resources`

## References 
**Hahn Discrete Orthogonal Polynomials** 
1. [Mesbah, A., Berrahou, A., Hammouchi, H., Berbia, H., Qjidaa, H., & Daoudi, M. (2019). Lip Reading with Hahn Convolutional Neural Networks. Image and Vision Computing. doi:10.1016/j.imavis.2019.04.010](https://www.sciencedirect.com/science/article/abs/pii/S0262885619300605)

2. [Hongqing Zhu, Huazhong Shu, Jian Zhou, Limin Luo, Jean-Louis Coatrieux. Image analysis by discrete orthogonal dual Hahn moments. Pattern Recognition Letters, Elsevier, 2007, 28 (13), pp.1688-1704. ff10.1016/j.patrec.2007.04.013ff. ffinserm-00189813f](https://www.hal.inserm.fr/inserm-00189813/file/Image_analysis_Hahn.pdf)

3. [Nikiforov, Arnold F.; Uvarov, Vasilii B. (1988). Special Functions of Mathematical Physics || . , 10.1007/978-1-4757-1595-8(), –. doi:10.1007/978-1-4757-1595-8](https://books.google.com.ng/books/about/Special_Functions_of_Mathematical_Physic.html?id=wMbeBwAAQBAJ&redir_esc=y)

4. [Gamma function](https://en.wikipedia.org/wiki/Gamma_function)