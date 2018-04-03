##the wp of  N1ctf    null   

简单记录下这道题：
思路比较巧妙，是一道关于多线程堆的利用。
主要是记录下调试过程中遇到的坑点，警戒自己。

####利用思路
不断malloc去扩展线程堆，当线程堆扩展到64M对齐时，若此时继续malloc，则会mmap出一个64M空间新堆，继续malloc，可以使2个堆块相邻。

```c
0x00007f8560000000 0x00007f8568000000 rw-p	mapped
0x00007f8568000000 0x00007f856c000000 rw-p	mapped
```
新的堆在低地址，top chunk在新heap的尾部。那么通过一次heap overflow就可以覆写旧堆的东西。
堆上首先存的是heap_info数据结构：

``` c
typedef struct _heap_info {mstate ar_ptr; /* Arena for this heap. */
struct _heap_info *prev; /* Previous heap. */ 
size_t size; /* Current size in bytes. */
size_t mprotect_size; /* Size in bytes that has been mprotectedPROT_READ|PROT_WRITE. *//* Make sure the following data is properly aligned, particularlythat sizeof (heap_info) + 2 * SIZE_SZ is a multiple of     MALLOC_ALIGNMENT. */char pad[-6 * SIZE_SZ & MALLOC_ALIGN_MASK]; 
} heap_info;
```
紧跟着就是`ar_ptr`所指向的`malloc_state` :

```c
struct malloc_state {  /* Serialize access.  */  mutex_t mutex;/* Flags (formerly in max_fast). */int flags;#if THREAD_STATS/* Statistics for locking. Only used if THREAD_STATS is defined. */ long stat_lock_direct, stat_lock_loop, stat_lock_wait;#endif  /* Fastbins */mfastbinptr fastbinsY[NFASTBINS];/* Base of the topmost chunk -- not otherwise kept in a bin */  mchunkptr        top;/* The remainder from the most recent split of a small request */mchunkptr last_remainder;/* Normal bins packed as described above */mchunkptr        bins[NBINS * 2 - 2];/* Bitmap of bins */
unsigned int binmap[BINMAPSIZE];/* Linked list */  struct malloc_state *next;#ifdef PER_THREAD/* Linked list for free arenas. */ struct malloc_state *next_free;#endif/* Memory allocated from the system in this arena. */INTERNAL_SIZE_T system_mem; INTERNAL_SIZE_T max_system_mem;};
```
然后只需通过堆溢出修改fastbinY即可。
因为fastbin取数据时没有对齐检测（但会检查size是不是当当前所在bin的size范围内），那么想办法在0x602038之前截断一个存有类似0x7f的地址，可以修改函数指针为system_plt即可。


####调式过程中遇到的坑

* 一开始无论怎么调在2个heap之间都会有gap，经过大神指点后了解到不应该直接malloc 0x4000，因为heap扩展时是页对齐的，也就是说一次扩展heap的大小是0x1000。所以一次malloc 0x1000是不会出现gap的。
*  和上个问题类似，当时，我好不容易将2个heap弄成相邻，但是heap之间的gap变成了64M，很郁闷，然后就想原因。后面觉得应该是thread_arena里的第一个heap后面剩了一个chunk没有0x1000对齐，想办法malloc掉这个chunk的大小就行了。

    
