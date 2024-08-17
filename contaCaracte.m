im1 = imread('ContarCaracteres.png');

x = 100;
y = 50;
largura = 200;
altura = 150;

imagem_recortada = imcrop(im1, [x y largura altura]);
imshow(imagem_recortada);
