#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <arpa/inet.h>

int main()
{
     int listenfd,connfd;
     int listenfd = socket(AF_INET,SOCK_STREAM,0);
     if(listenfd == -1)
     {
          perror("socket");
          return -1;  
     }
     
     int on = 1;
     int ret = setsockopt(listenfd,SOL_SOCKET,SO_REUSEADDR,&on,sizeof(on));
     if(-1 == ret){
         perror("setsockopt");
         return -1;
     }

     struct sockaddr_in saddr,caddr;
     saddr.sin_family = AF_INET;
     saddr.sin_port = htons(8888);
     //获取本机地址  
     saddr.sin_addr.s_addr = htonl(INADDR_ANY);
     //手动填写地址
     //saddr.sin_addr.s_addr = inet_addr("127.0.0.1");
     
     ret = bind(listenfd,(struct sockaddr *)(&saddr),sizeof(saddr));
     if(-1 == ret){
          perror("bind");
          return -1;
    }  
     ret = listen(listenfd, 5);
     if(-1 == ret){
          perror("listen");
          return -1;
     }

     char buf[1024];
     addrlen = sizeof(caddr);
     while(1)
     {
             connfd = accept(listenfd, (struct sockaddr *)&caddr, &addrlen);
             if(-1 == ret){
                    perror("accept");
                    return -1;
             }
             inet_ntop(AF_INET,&caddr.sin_addr,cip,INET_ADDRSTRLEN);
             printf("client ip = %s, port = %d\n",cip,ntohs(caddr.sin_port));　　//打印客户端的ip和端口
             memset(buf,0,sizeof(buf));
             ret = read(connfd, buf, sizeof(buf));
             if(-1 == ret){
                    perror("read");
                    return -1;
             }
             ret = write(connfd,buf,sizeof(buf));
             if(-1 == ret){
                    perror("write");
                    return -1;
            }
     }
}
