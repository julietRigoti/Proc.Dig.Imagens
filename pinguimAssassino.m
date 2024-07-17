imagem = imread('file:///home/juliet/Documents/CC/PDI/tchola.jpg');

img = rgb2gray(imagem);  % Converter para escala de cinza, se necess?rio

% Definir os kernels
kernel_media = ones(7, 7) / 49; % correto estar assim

% Aplicar os filtros
img_media = conv2(double(img), kernel_media, 'same');

% Exibir as imagens
subplot(1, 3, 1);
imshow(img);
title('Imagem Original');

subplot(1, 3, 2);
imshow(img_media, []);
title('Filtro de M‚dia');
