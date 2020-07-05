python网络编程相关
========
网络基础
-----
### 软件开发的架构<br>
* C/S架构：即客户端/服务器端架构,需要用户安装exe程序才能运行<br>
* B/S架构：即浏览器端/服务器端架构,不需要用户额外安装exe程序，在浏览器上经过http请求资源<br>
### OSI七层模型与TCP/IP五层模型<br>
* OSI七层模型具体划分为应用层、表示层、会话层、传输层、网络层、数据链路层、物理层
* TCP/IP五层模型具体划分为应用层、传输层、网络层、数据链路层、物理层
### 以太网/广域网  交换机/路由器
* 以太网<br>
以太网是一种局域网技术，IEEE组织的IEEE 802.3标准制定了以太网的技术标准<br>
以太网是广播类型的网络，支持一对多的通讯方式，而PPP网是点对点的<br>
>>关于广播：
>>主机之间“一对所有”的通讯模式，网络对其中每一台主机发出的信号都进行无条件复制并转发，所有主机都可以接收到所有信息（不管你是否需要），由于其不用路径选择，所以其网络成本可以很低廉<br>
* 交换机<br>
交换机将多台主机通过网线连接起来，形成局域网<br>
交换机用于同一网络内部数据的快速传输<br>
转发决策通过查看二层头部完成，依据对象为MAC地址（物理地址）<br>
转发不需要修改数据帧<br>
>>前面提到的交换机是传统的二层交换机，工作在数据链路层，还有三层交换机，工作在网络层，具备了部分路由器的功能，最重要目的是加快大型局域网内部的数据交换，能够做到一次路由，多次转发。三层交换技术就是二层交换技术+三层转发技术
* 路由器<br>
路由器将交换机组好的局域网相互连接起来，或者连入Internet<br>
路由器用于不同网络之间的数据交换<br>
转发决策通过查看三层头部完成，依据对象为IP地址（网络地址）<br>
转发需要修改 TTL ，IP 头部校验和需要重新计算，数据帧需要重新封装<br>
## 代码实现
1.多进程（线程）+socket套接字实现并发服务器<br>
2.进程间通信（IPC）<br>
  （1）消息传递 ----> 管道，pipe，消息队列<br>
  （2）同步---->互斥锁，条件变量，读写锁，信号量<br>
  （3）共享内存区<br>
3.各种I/O<br>
  阻塞式I/O，非阻塞式I/O，I/O复用，信号驱动式I/O，异步I/O
