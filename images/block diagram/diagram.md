```mermaid
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
    n3["Object localization"] --> n15["Obtain the largest bounding box and its center position"]
    A["Capture RGB frame"] --> n6["Timestamp"] & n21["Image/Frame"]
    n6 --> B("Timestamp comparison")
    n1["Capture LiDAR frame"] --> n7["Timestamp"] & n22["Distance"]
    n7 --> B
    C["Dictionary storage of timestamp matched camera and LiDAR frames"] --> n9["Time-synchronized camera frame"] & n10["Time-synchronized LiDAR frame"]
    n17["If distance &gt;= 1000"] -- True --> n19["No output"]
    n20["Buzzer calculation + frequency matched with distance"] --> n13["Center side: position in center (213-426), both buzzers buzzes"] & n12["Right side: position on right (426-640), right buzzer buzzes"] & n14["Left side: position on left (0-213), left buzzer buzzes with frequency relative to distance"]
    n15 --> n20
    B --> C
    n10 --> n22
    n22 --> n17
    n17 -- False --> n20
    n13 --> n23["Trigger Buzzer"]
    n12 --> n23
    n14 --> n23
    n9 --> n24["Object detection"]
    n24 --> n3
    n21 --> n9

    n3@{ shape: event}
    n15@{ shape: rounded}
    A@{ shape: lean-r}
    n1@{ shape: lean-r}
    C@{ shape: event}
    n17@{ shape: diam}
    n20@{ shape: rounded}
    n13@{ shape: rounded}
    n12@{ shape: rounded}
    n14@{ shape: rounded}
    n24@{ shape: rounded}
     a1:::capture
     a2:::data
     a3:::process
     a4:::output
    classDef capture fill:#FFCDD2,stroke:#F44336
    classDef data fill:#FFF9C4,stroke:#FBC02D
    classDef process fill:#C8E6C9,stroke:#388E3C
    classDef output fill:#BBDEFB,stroke:#1976D2
    style n3 fill:#C8E6C9
    style n15 fill:#C8E6C9
    style A fill:#FFCDD2
    style n6 fill:#FFF9C4
    style n21 fill:#FFF9C4
    style B fill:#C8E6C9
    style n1 fill:#FFCDD2
    style n7 fill:#FFF9C4
    style n22 color:#000000,fill:#FFF9C4
    style C fill:#C8E6C9
    style n9 fill:#FFF9C4
    style n10 fill:#FFF9C4
    style n17 fill:#C8E6C9
    style n19 fill:#BBDEFB
    style n20 color:#000000,fill:#C8E6C9
    style n13 fill:#C8E6C9
    style n12 fill:#C8E6C9
    style n14 fill:#C8E6C9
    style n24 fill:#C8E6C9
    style n23 fill:#BBDEFB
    ```

    #todo add a new actuator description 