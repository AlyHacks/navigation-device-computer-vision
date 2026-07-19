flowchart TB
    n3["Area of largest boundary in frame"] --> n15["Center point position of largest boundary"]
    A["Capture RGB frame"] --> n5["Object detection"]
    n5 --> n6["timestamp, results"]
    n6 --> B("Timestamp comparison")
    n1["Capture sensor frame"] --> n7["timestamp, distance"]
    n7 --> B
    B --> n8["RGB and sensor frame with closest timestamp"]
    n8 --> C["Fused results"]
    C --> n9["Correct camera frame"] & n10["Correct sensor frame"]
    n9 --> n3
    n10 --> n11["Distance of sensor frame"]
    n11 --> n17["No output if distance &gt;= 1000"] & n18["If distance&lt;1000 then buzzer buzzes with frequency dependent of distance"]
    n15 --> n16["Classify position of object"]
    n16 --> n12["Right side: position on right (426-640), right buzzer buzzes"] & n14["Left side: position on left (0-213), left buzzer buzzes"] & n13["Center side: position in center (213-426), both buzzers buzzes"]
    n12 --> n4["Buzzer output"]
    n14 --> n4
    n13 --> n4
    n18 --> n4

    n3@{ shape: event}
    n15@{ shape: rounded}
    A@{ shape: lean-r}
    n5@{ shape: rounded}
    n1@{ shape: lean-r}
    C@{ shape: event}
    n16@{ shape: rounded}
    n12@{ shape: rounded}
    n14@{ shape: rounded}
    n13@{ shape: rounded}
    style n3 fill:#C8E6C9
    style n15 fill:#C8E6C9
    style A fill:#FFCDD2
    style n5 fill:#C8E6C9
    style n6 fill:#FFF9C4
    style B fill:#C8E6C9
    style n1 fill:#FFCDD2
    style n7 fill:#FFF9C4
    style n8 fill:#FFF9C4
    style C fill:#C8E6C9
    style n9 fill:#FFF9C4
    style n10 fill:#FFF9C4
    style n11 fill:#FFF9C4
    style n4 fill:#BBDEFB
    style n16 fill:#C8E6C9
    style n12 fill:#C8E6C9
    style n14 fill:#C8E6C9
    style n13 fill:#C8E6C9