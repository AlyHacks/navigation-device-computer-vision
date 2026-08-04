---
config:
  layout: dagre
---
flowchart TB
 subgraph Legend["Legend"]
    direction TB
        a1["🔴 Capture step"]
        a2["🟡 Data/result node"]
        a3["🟢 Processing step"]
        a4["🔵 Output/Action"]
  end
    A["RGB sensor reading"] --> n6["Timestamp"] & n21["Camera Buffer"]
    n6 --> B("Timestamp comparison")
    n1["LiDAR sensor reading"] --> n7["Timestamp"] & n10["Time-synchronized LiDAR frame"]
    n7 --> B
    C["Dictionary of timestamp-matched camera and LiDAR frames"] --> n9["Time-synchronized camera frame"]
    n17["If distance &gt;= 1000"] -- True --> n19["No output"]
    n20["Buzzer calculation + frequency matched with distance"] --> n13["Center side: position in center (213-426), both buzzers buzzes"] & n12["Right side: position on right (426-640), right buzzer buzzes"] & n14["Left side: position on left (0-213), left buzzer buzzes with frequency relative to distance"]
    B --> C
    n9 --> n24["Object detected"]
    n24 -- Yes --> n3["Object localization"]
    n24 -- No --> n27["Both buzzers buzz with frequency matched with distance"]
    n21 --> C
    n25["Position index"] --> n20
    n17 -- False --> n26["Distance output"]
    n26 --> n20
    n10 -- <br> --> n17
    n3 --> n25

    A@{ shape: lean-r}
    n1@{ shape: lean-r}
    C@{ shape: event}
    n17@{ shape: diam}
    n20@{ shape: rounded}
    n13@{ shape: rect}
    n12@{ shape: rect}
    n14@{ shape: rect}
    n24@{ shape: decision}
    n3@{ shape: event}
     a1:::capture
     a2:::data
     a3:::process
     a4:::output
    classDef capture fill:#FFCDD2,stroke:#F44336
    classDef data fill:#FFF9C4,stroke:#FBC02D
    classDef process fill:#C8E6C9,stroke:#388E3C
    classDef output fill:#BBDEFB,stroke:#1976D2
    style A fill:#FFCDD2
    style n6 fill:#FFF9C4
    style n21 fill:#FFF9C4
    style B fill:#C8E6C9
    style n1 fill:#FFCDD2
    style n7 fill:#FFF9C4
    style n10 fill:#FFF9C4
    style C fill:#C8E6C9
    style n9 fill:#FFF9C4
    style n17 fill:#C8E6C9
    style n19 fill:#BBDEFB
    style n20 color:#000000,fill:#C8E6C9
    style n13 fill:#BBDEFB
    style n12 fill:#BBDEFB
    style n14 fill:#BBDEFB
    style n24 fill:#C8E6C9
    style n3 fill:#C8E6C9
    style n27 fill:#BBDEFB
    style n25 fill:#FFF9C4
    style n26 fill:#FFF9C4