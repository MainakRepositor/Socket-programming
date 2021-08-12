#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>

void error(const char *msg)
{
   perror(msg);
   exit(0);
}

int main(int argc, char *argv[])
{
  if(argc < 2)
  {
   fprintf(stderr,"Port number is required. Program terminated!\n");
   exit(1);
   }
   
   int sockfd, newsockfd, portnum, m;
   char buffer[255];
   struct sockaddr_in serv_addr, cli_addr;
   socklen_t clilen;
   sockfd = socket(AF_INET, SOCK_STREAM, 0);
   if(sockfd < 0)
     {
     error("Error opening socket");
     }
   bzero((char *) &serv_addr, sizeof(serv_addr));
   portnum = atoi(argv[1]);
   
   serv_addr.sin_family = AF_INET;
   serv_addr.sin_addr.s_addr = INADDR_ANY;
   serv_addr.sin_port = htons(portnum);
   
   if(bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr))<0)
   {
    error("Binding Failed!");
    }
   
   listen(sockfd, 6);
   clilen = sizeof(cli_addr);
   newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
   
   if(newsockfd < 0)
      error("Error on Acceptance!");
      
   
   while(1)
   {
   bzero(buffer,255);
   m = read(newsockfd, buffer, 255);
   if(m<0)
     error ("Error on Reading!");
   
   printf("Client : %s\n",buffer);
   bzero(buffer,255);
   fgets(buffer,255,stdin);
   m = write(newsockfd, buffer, strlen(buffer));
   
   if(m < 0)
      error("Error on Writing");
   
   int i = strncmp("Bye",buffer,3);
   if(i==0)
   break;
   }
   close(newsockfd);
   close(sockfd);
   
   return 0;
 }