# mini-os-simulator

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
- Priority : 1, 2, 3 (Init, User, System)

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
### Outline
- 3-level priority scheduler 
- Use preemptive round-robin scheduling within level
- [Reference to preemtive round-robin scheduling](http://www.read.cs.ucla.edu/111/2007fall/notes/lec7)
- Time sharing is simulated by a function call
	- if happens, the process will be placed in the tail
- Init process serves two purposes: dummy process: lowerst priority, never blocked -root of process creation tree
- Preemption
	- Change status of p to running (status of self already changed to ready/blocked)
	- Context switch - output of nmae of running process

	Scheduler() {
		find highest priority process p
		if (self->priority < p->priority ||  # create / release
			self->Status.Type != 'running' ||  # request / time-out
			self == NIL)  # NIL
			premep(p, self)  # print the new running process p here
	}

### Time-out

	Time_out() {
		find running process p
		remove(RL, p)
		q->Status.Type = 'ready'
		insert(RL, q)
		Scheduler
	}