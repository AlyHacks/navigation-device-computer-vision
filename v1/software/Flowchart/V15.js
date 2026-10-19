---
config:
  layout: dagre
id: 8cb0ddeb-12c9-4671-9e85-eb5b82f8d28e
---
flowchart TB
 subgraph Legend["Legend"]
    direction TB
        a1["🔴 Capture step"]
        a2["🟡 Data/result node"]
        a3["🟢 Processing step"]
        a4["🔵 Output/Action"]
  end
    A["RGB sensor reading"] --> n21["Camera Buffer"] & n6["Timestamp"]
    n6 --> B("Timestamp comparison")
    n1["LiDAR sensor reading"] --> n7["Timestamp"] & n10["Time-synchronized LiDAR frame"]
    n7 --> B
    C["Dictionary of timestamp-matched camera and LiDAR frames"] --> n9["Time-synchronized camera frame"]
    B --> C
    n9 --> n43["Distance &lt; 1000"]
    n21 --> C
    n43 -- NO --> n44["No output"]
    n43 -- YES --> n46["Object detected?"]
    n46 -- YES --> n52["Object localization"]
    n46 -- NO --> n38["Both buzzers output buzzing frequency relative to distance"]
    n52 --> n53["Position index"]
    n53 --> n54@{ label: "<span style=\"background-color:\">If 0&lt;index&lt;320, left buzzer buzzes with frequency relative to distance</span>" } & n55["If 320&lt;index&lt;640, right buzzer buzzes with frequency relative to distance"]
    n10 --> n43

    A@{ shape: lean-r}
    n1@{ shape: lean-r}
    C@{ shape: event}
    n43@{ shape: diam}
    n46@{ shape: rounded}
    n52@{ shape: rounded}
    n54@{ shape: rect}
    n55@{ shape: rect}
     a1:::capture
     a2:::data
     a3:::process
     a4:::output
    classDef capture fill:#FFCDD2,stroke:#F44336
    classDef data fill:#FFF9C4,stroke:#FBC02D
    classDef process fill:#C8E6C9,stroke:#388E3C
    classDef output fill:#BBDEFB,stroke:#1976D2
    style A fill:#FFCDD2
    style n21 fill:#FFF9C4
    style n6 fill:#FFF9C4
    style B fill:#C8E6C9
    style n1 fill:#FFCDD2
    style n7 fill:#FFF9C4
    style n10 fill:#FFF9C4
    style C fill:#C8E6C9
    style n9 fill:#FFF9C4
    style n43 fill:#C8E6C9
    style n44 fill:#BBDEFB
    style n46 fill:#C8E6C9
    style n52 fill:#C8E6C9
    style n38 fill:#BBDEFB
    style n53 fill:#FFF9C4
    style n54 fill:#BBDEFB
    style n55 fill:#BBDEFB