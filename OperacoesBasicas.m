%% Exemplos b�sicos
Im1=ones(256,256);
imshow(Im1);

%Im1(128,128)=0;

Im1(50:100,50:206)=0;
Im1(100:206,103:153)=0;
figure, imshow(Im1);

%%
Im2=Im1;
for c = 50:206
    for r = 50:100
        Im2(r,c) = 0;
    end
end
figure, imshow(Im2);

%% Exemplos de opera��es b�sicas com imagens;
i=imread('Map-of-Middle-Earth-lord-of-the-rings-2329809-1600-1200.jpg');
i=rgb2gray(i);
figure('Name','Original');
imshow(i);

i(100:200,100:1500,:)=0;
figure('Name','Alterada');
imshow(i);

% imadjust

%adi��o
i1=i+50;
figure('Name','Adi��o');
imshow(i1);
%subtra��o
i2=i-50;
figure('Name','Subtra��o');
imshow(i2);

%multiplica��o
i3=i*2;
figure('Name','Multiplica��o');
imshow(i3);

%divis�o
i4=i/2;
figure('Name','Divis�o');
imshow(i4);

%complemento
i5=255-i;
figure('Name','Complemento');
imshow(i5);

%% subtra��o exemplo pr�tico

I = imread('rice.png');
figure('Name', 'Original: Ilumina��o n�o uniforme');
imshow(I)
I2=im2bw(I);
figure(),imshow(I2);

background = imopen(I,strel('disk',15));

figure('Name', 'Fundo Ilumina��o(aproxima��o)');
imshow(background);

% Display the Background Approximation as a Surface
figure, surf(double(background(1:8:end,1:8:end))),zlim([0 255]);
set(gca,'ydir','reverse');

I2 = I - background;

figure('Name', 'Resultado da subtra��o');
imshow(I2)

I3=im2bw(I2,0.3);
figure(),imshow(I3);


%%
figure('Name', 'Testes Limiariza��o');
subplot(2,3,1);
imshow(I);
title('original');
subplot(2,3,4);
imshow(I2);
title('uniformizada');

subplot(2,3,2);
imshow(im2bw(I,0.6));
title('T=0.5');
subplot(2,3,5);
imshow(im2bw(I2,0.6));
title('T=0.5');

subplot(2,3,3);
imshow(im2bw(I,0.2));
title('T=0.2');
subplot(2,3,6);
imshow(im2bw(I2,0.2));
title('T=0.2');

%% subplot
figure('Name', 'Exemplo Subplot com histograma');
subplot(2,2,1);
imshow(I);
title('original');
subplot(2,2,3);
imshow(I2);
title('uniformizada');

subplot(2,2,2);
imhist(I);
title('imhist');
subplot(2,2,4);
imhist(I2);
title('imhist');

