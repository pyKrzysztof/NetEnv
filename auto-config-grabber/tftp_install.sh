sudo apt-get install xinetd tftpd tftp
echo "service tftp
{
protocol        = udp
port            = 69
socket_type     = dgram
wait            = yes
user            = nobody
server          = /usr/sbin/in.tftpd
server_args     = $1
disable         = no
}" > /etc/xinetd.d/tftp

sudo mkdir $1
sudo chmod -R 777 $1
sudo chown -R nobody $1

sudo /etc/init.d/xinetd stop
sudo /etc/init.d/xinetd start