# mini-os-simulator: Project 1

## 1. Process and Resource Manager
### Functionality:
- process : create / destroy; datastructure: PCB
- resource : request / release
- time-out interrupt : scheduling, cycle through different resources
- multi-unit resources : every unit would have more than one unit
- error checking : dealing with potential errors

### Simulation:
- without actual hardware, we simulate the process on terminal (input/output file)
	- currently running process and 
	- the hardware causing interrupts

### Organization:
- Shell
	- reads command from terminal or text file
	- invokes kernel function
	- displays reply ( termianl or output file)
		- running process
		- errors

### Workflow:
1. Input thruogh Termianl / Test Files
2. Get command wirh args, invoke command with args
3. Operates Process / Resource Manager
4. Receive response, display response

### Components:
a. Interface: 
	- termianl / test files
b. Driver:
	- looping for getting command with args (i.e. cr A 1)
	- invoking command with args
	- receive response
	- display response
c. Process/Resource Manager:

### Shell Example:
	> cr A 1 
	Process A is running 
	> cr B 2 
	Process B is running 
	> cr C 1 
	Process B is running 
	> req R1, 1 
	Process B is blocked; process A is running 



## 2. Implementation: Process
### States and Operations
- States: Ready, Running, Block
- Possible Operations:

| Ops       | State From            | State To  |
| :-------: |:---------------------:| :--------:|
| Create    | (None)                | Ready     |
| Destroy   | Running/Ready/Blocked |   (None)  |
| Request   | Running               | Blocked   |
| Release   | Blocked               | Ready     |
| Time_Out  | Running               | Ready     |
| Scheduler1| Ready                 | Running   |
| Scheduler2| Running               | Ready     |

### Process Control Block (PCB)
- PID
- Other Resources : Linked List like, pointing to resource control block, which results of requets
- Status : Type (Running/Ready/Blocked)& List (back pointer to either Ready List (if process running) Blocked List (otherwise))
- Creation Tree : Parent (pointing to parent PCB)/Child (pointing children)
- Priority : 0, 1, 2 (Init, User, System)

### Ready List
- 2 (system), 1 (user), 0 (init)
- Priorities don't change in a session
- Every process is either on Ready List or Blocked List
- When start a session, a process ties to init level to begin
- Each level of priorities may have any number of processes

### Create

	Create(initialization params) {
		create PCB data struct
		initialize PCB using params
		link PCB to creation tree
		insert(RL, PCB)
		scheduler()
	}

- Init process is created at start-up & can create first system or user process
- Any new or released process is inserted at the end of the queue (RL)

### Destroy

	Destroy (pid) {
		get pointer p to PCB using pid
		Kill_Tree(p)
		Scheduler()
	}

	Kill_Tree(p) {
		for all child processes q Kill Tree(q)
		free resources
		delete PCb and update all the pointers
	}

- Process can be destroyed by any of its ancesters or by itself (exit)



## 3. Representation of Resources
### Configuration
- There is a fixed set of resources
- Resource Control Block (RCB)
	- RID
	- Status : coutner for number of free units, K initial units (fixed), U currently available units (decreases/increases)
	- Waiting_List : list of blocked processes

### Request Resources (1-unit resource  # n-units resources)

	Request(rid) {
		r = Get_RCB(rid)
		if (r->Status == 'free') {  # u > n, where available # of units, u, and requesting # of units, n
			r->Status == 'allocated'  # u = u - n
			insert(self->Other_Resources, r)  # n units of resource r
		} else {
			self->Status.Type = 'blocked'
			self->Status.Link = r
			remove(RL, self)
			isnert(r->Waiting_List, self)
			Scheduler()
		}
	}

### Release Resources (1-unit resource  # n-units resources)

	Release(rid, n) {  # n is the number of units of resources to release
		r = Get_RCB(rid)
		remove(self->Other_Resources, r)  # u = u + n
		if (r->Waiting_list == 'NIL') {  # while (r->Waiting_List != NIL && u >= req)
			r->Status = 'free'  # u = u - req
		} else {  # ---del this line----
			remove(r->Waiting_List, q) 
			q->Status.Type = 'ready'
			q->Status.List = RL
			insert(q->Other_Resources, r)
			insert(RL, q)
			Scheduler()
		}
	}

- all requests are satisfied in strict FIFO order



## 4. Scheduling
### Specs
- 3-level priority scheduler 
- Use preemptive round-robin scheduling within level
- [Reference to preemtive round-robin scheduling](http://www.read.cs.ucla.edu/111/2007fall/notes/lec7)
- Time sharing is simulated by a function call
	- if happens, the process will be placed in the tail
- Init process serves two purposes: dummy process: lowerst priority, never blocked -root of process creation tree
- Preemption
	- Change status of p to running (status of self already changed to ready/blocked)
	- Context switch - output of nmae of running process

### Implementation

	Scheduler() {
		find highest priority process p
		if (self->priority < p->priority ||  self->Status.Type != 'running' || self == NIL)  
			premep(p, self)  # print the new running process p here
	}

	Time_out() {
		find running process p
		remove(RL, p)
		q->Status.Type = 'ready'
		insert(RL, q)
		Scheduler
	}



## 5. Presentation/Shell Script
### Mandatry Commands
- init
- cr <name> <priority>
	- name: single char
	- priority: 0, 1, or 2
- de <name>
	- name: single char
- req <resource name> <# of units>
	- resource name: R1, R2, R3, or R4
- rel <resource name> <# of units>
	- resource name: R1, R2, R3, or R4
- to
	- 'time-out'

### Optional Commands
- list all processes and its status
- list all resources and its status
- provide information about a given process
- provide information about a given resource



## 6. Summary
### Tasks
- Design/implement the process and resource manager
	- data structure and functions
- Design/implement the driver (shell)
	- command language and interpreter
- Instantiate the manager to include at a start-up:
	- A Ready List with 3 priorities
	- A single process, Init
	- 4 resources labeled: R1, R2, R3, R4 (each Ri has i units)
	- An IO resource
- Submit program for testing and documentation for evaluation

[To refer to test examples, watch this video again](http://replay.uci.edu/public/summer2013/Bic-kernel-projE_-_MP4_with_Smart_Player_(Large)_-_20130807_01.20.09AM.html)

[Official project spec](http://www.ics.uci.edu/~bic/courses/NUS-OS/PROOFS/bicpr02v2.pdf)

[Reading](http://www.ics.uci.edu/~bic/courses/NUS-OS/PROOFS/bicc04v2.pdf)

[Protocol - Make sure following this](http://www.ics.uci.edu/~bic/courses/143B/Process-Project/protocol.pdf)


## 7. Learnings
- [Python Classes Basics](https://python.swaroopch.com/oop.html)
- [Python Linked List Implementation](http://stackoverflow.com/questions/280243/python-linked-list)
- [OS Scheduling](https://www.cs.rutgers.edu/~pxk/416/notes/07-scheduling.html)
- [Deadlock Intro](http://www.cs.yale.edu/homes/aspnes/pinewiki/Deadlock.html)
- [Python Library Collections Doc](https://docs.python.org/2/library/collections.html#collections.deque)


# mini-os-simulator: Project 2
Beign project 2

## 1. Project Description A
- Goal: compare different scheduling algorithms
- assume single processor
- scheduling algo determines which process should run at each time step
- minimize turnaround time:
	- turnaround time: average of the real time of all the processes in the system
	- for all process i, sum += r_i where r_i = t_i (total time: CPU time which the process running)+ waiting time (the process not running) or finish time - start time of a process i and n = the number of processes 

## 2. Project Description B
- Implement and compere: 
	- FIFO (First-In-First-Out): Process entered first runs first
	- SJF (Shortest Job First): Process with shorter running time runs first
	- SRT (Shortest Remaining Time): SJF but preemptive. If new process has less running time than the remaining running time of currently running process, the new process runs first.
	- MLF (Multi-Level Feedback Queue): n priorities, each n level has Time Slice (TS) TS_n-1 = 2*TS_n where TS_n = 1
- Inputs: a series of arrival and total service time
- Outputs for each algorithms:
	- the real time r_i of each process
	- average turnaround time
- Output Format: T r_1 r_2 .. r_n
	- T: average turn around time
	- each r_i is the real time of process i

## 3. Testing Procedure
- For each algorithm:
	- read integer pairs ar_i (arrival time) and t_i (required running time) from file input.txt on memory stick
	- ourput results into a file name STUDENT_ID.txt to the same memory stick
- Output flie should contain 4 separate lines of the form
	- T r_1 r_2 .. r_n

## 4. References 
- [The Lecture Video including Testing Example](http://replay.uci.edu/public/winter2015/Bic-proj-schedA_-_20150112_122322_15.html)
- [Official Project Description](http://www.ics.uci.edu/~bic/courses/143B/Sched-project/Description.pdf)
- [Protocol to Follow](http://www.ics.uci.edu/~bic/courses/143B/Sched-project/Protocol.pdf)



# mini-os-simulater: Project 3

## 1. Assignment Outline
- VM using segmentatoin and paging
- managin segment and page tables in a simulated main memory 
- It accepts Virtual Addresses and translates them into Physical Addresses
- It utilizes translation look-aside buffeer (TLB) to make the process more efficient

## 2. [Virtual Memory Basics Note](http://www.toves.org/books/vm/)
### Intro
- The system stores the official copy of memory on disk and caches only the most frequently used data in RAM.
- To make this workable, we break virtual memory into chunks called pages; a typical page size is four kilobytes.
- We also break RAM into page frames, each the same size as a page, ready to hold any page of virtual memory.
- The system also maintains a page table, stored in RAM, which is an array of entries, one for each page, storing information about the page

![alt tag](https://cloud.githubusercontent.com/assets/1572847/23149627/2cc123bc-f7a2-11e6-87f8-fe8ee69ddc6e.png)

### Example
- The size of one VM is 15 bits long, which 32k bytes.
	- 8 pages / 1 VM * 4k bytes / page = 32k bytes / 1 VM
- the RAM's page table is correspondants of the virtual memory
	- The data of page 0 in VM is stored in the frame 2 in RAM
	- The data of page 2 in VM is stored in the frame 3 in RAM
	- The data of page 4 in VM is stored in the frame 1 in RAM

### Address Translation
- From CPU, it asks utilizing a data referencing VM, not actual RAM PA (Physical Address)
- Since VM does not contain the actual data, we need to translate the VM to PM
- Procedure:
	1. CPU breaks the adress into the first three bits, which represents a particular page (2^3 = 8) and the rest of twelve bits, which represents giving the offset offs within the page.
	2. CPU looks into the page table and try to fetch the corresponding frame
	3. IF page is not in the frame in RAM, it initiates the page fault.
	4. ELSE, CPU loads from the memory address offs within page frame f

### Parge Table Format
- A Page Table contains multiple page entries
- Each entry, depending on its design, contains specific bits for each purpose.
	- Load Bit: a bit to represents wthether the page is currently loaded onto memory or not
	- Frame Bits: bits to locate which page frame contains the page.
	- Dirty Bit: a bit specifies whether the page in memory has been altered since being loaded onto memory.
	This is useful to reduce the cost of writing back to disk when the page is removed from the memory.
	This makes sure it wirte back to the disk only if the page is updated since it has been loaded onto memory.
	- Referenced Bit: this is set as 1 whenever the page is accessed.
	OS periodically visits this bit to see whether it's 1 and set it 0.
	IF it's 1, then it indicates the page recently accesessed since preivous prediodic checking mentioned above.
	OTHERWISE, it has not been utilized so it might be good to empty the page from frame to allocate space for another page.


