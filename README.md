## instala dependencias
#### python3 -m pip install requirements.txt

## seta variaveis de ambiente (exemplo abaixo é no linux)
#### export BIGIP_USER=seu_usuario_no_bigip
#### export BIGIP_PASS=sua_senha

## editar o arquivo main.py com os devidos pools e IPs de nodes a serem adicionados ou removidos

## executa o script para ingressar/remover servidores nos respectivos pools
#### python3 main.py
