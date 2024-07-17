% Carregue as imagens
#imagem_base = imread('file:///home/juliet/Documents/CC/PDI/tsunadeDeJuliet.jpg');
#imagem_bandeira = imread('file:///home/juliet/Documents/CC/PDI/bandeiraBi.jpg');

% Converta as imagens para escala de cinza
#imagem_base_cinza = mat2gray(imagem_base);
#imshow(imagem_base_cinza);
#imagem_bandeira_cinza = mat2gray(imagem_bandeira);

% Crie a máscara de inversão
#mascara_invertida = imcomplement(imagem_bandeira_cinza);

% Combine as imagens com transparência
#alpha = 0.5;
#imagem_final = imagem_base_cinza .* (1 - alpha) + mascara_invertida .* alpha;

% Converta para RGB
#imagem_final_rgb = im2uint8(imagem_final);

% Exiba a imagem final
#imshow(imagem_final_rgb);

% Carregar a imagem da Tsunade
imagem = imread('file:///home/juliet/Documents/CC/PDI/tsunadeDeJuliet.jpg');

[altura, largura, ~] = size(imagem);

% Dividir a imagem em três partes iguais
terco = floor(altura / 3);

% Criar máscaras de cor com opacidade
opacidade = 0.7; % ajuste a opacidade conforme necessário (0 a 1)

% Aplicar rosa ao primeiro terço
mascara_rosa = imagem;
mascara_rosa(1:terco, :, 1) = opacidade * 255 + (1 - opacidade) * imagem(1:terco, :, 1); % R
mascara_rosa(1:terco, :, 2) = opacidade * 102 + (1 - opacidade) * imagem(1:terco, :, 2); % G
mascara_rosa(1:terco, :, 3) = opacidade * 204 + (1 - opacidade) * imagem(1:terco, :, 3); % B

% Aplicar roxo ao segundo terço
mascara_roxo = imagem;
mascara_roxo(terco+1:2*terco, :, 1) = opacidade * 153 + (1 - opacidade) * imagem(terco+1:2*terco, :, 1); % R
mascara_roxo(terco+1:2*terco, :, 2) = opacidade * 51 + (1 - opacidade) * imagem(terco+1:2*terco, :, 2); % G
mascara_roxo(terco+1:2*terco, :, 3) = opacidade * 255 + (1 - opacidade) * imagem(terco+1:2*terco, :, 3); % B

% Aplicar azul ao terceiro terço
mascara_azul = imagem;
mascara_azul(2*terco+1:end, :, 1) = opacidade * 0 + (1 - opacidade) * imagem(2*terco+1:end, :, 1); % R
mascara_azul(2*terco+1:end, :, 2) = opacidade * 102 + (1 - opacidade) * imagem(2*terco+1:end, :, 2); % G
mascara_azul(2*terco+1:end, :, 3) = opacidade * 204 + (1 - opacidade) * imagem(2*terco+1:end, :, 3); % B

% Combinar as máscaras para criar a imagem final
imagem_final = imagem;
imagem_final(1:terco, :, :) = mascara_rosa(1:terco, :, :);
imagem_final(terco+1:2*terco, :, :) = mascara_roxo(terco+1:2*terco, :, :);
imagem_final(2*terco+1:end, :, :) = mascara_azul(2*terco+1:end, :, :);

% Exibir a imagem final
imshow(imagem_final);



