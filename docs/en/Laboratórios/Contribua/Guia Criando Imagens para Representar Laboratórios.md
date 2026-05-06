# Guide: Creating Images to Represent Labs

This guide teaches how to create images representing network topologies for labs, using the <a target="_blank" href="http://draw.io/">Draw.io</a> template provided in the repository. The images must follow the project's visual identity and be saved in **SVG** format within the correct folder.

---

### 1. **Opening the Template**

In the root of the repository `docs/Templates`, you will find a <a target="_blank" href="http://draw.io/">**Draw.io**</a> template, which you can see below. Open the file, and you will see that it already contains all the components needed to create network topologies, including:

![Draw.io Template](../../../img/Template_redes_abertas.svg)

- **Application Cards**: Represent assets or protocols such as **Grafana** and **OpenConfig**.
- **Network Components**: Icons of **routers**, **switches,** and **servers**.

---

### 2. **Assembling the Topology**

1. **Add Network Components**: Copy and paste the icons of **routers**, **switches,** and **servers** from the component area of the template.
2. **Add Application Cards**: Position the cards that represent the assets/protocols in the topology.
3. **Connect the Components**: Use **lines** (for interconnections) and **arrows** (to point to the IPs) to connect the components and create the network structure.

### Style Specifications for the Topology

| Element | Specification |
|---|---|
| **Title Font** | **Font**: Times New Roman, **Size**: 28px |
| **Subtitle Font** | **Font**: Times New Roman, **Size**: 25px |
| **Connection Lines** | **Thickness**: 11px, **Type**: Straight lines (for interconnections) |
| **Arrows for IPs** | **Thickness**: 11px, **Type**: Arrows (to point to the IPs) |
| **Interface Boxes** | **Font Size**: 11px |

With these specifications, you ensure that the topologies follow the project's visual standard and are consistent with the rest of the documentation.

---

### 3. **Adding Interfaces and IPs**

1. **Create the Text Box for Interfaces**: For each connection, draw a square representing the interface.
2. **Add IP Property**:
    - Select the square.
    - Right-click and choose **Add/Edit Data**.
    - Click on **Add Property**, name it **ip**, and add the IP address of the interface.

When the mouse hovers over the square, the IP will be displayed as a tooltip.

---

### 4. **Saving the Image**

After finalizing the topology, save the image in **SVG** format:

1. **Save as SVG**: In <a target="_blank" href="http://draw.io/">**Draw.io**</a>, go to **File > Export As > svg**.
2. **Destination Folder**: Save the image in the `docs/img/labs_imgs/` folder.

!!! warning "Attention"
    Make sure to select **Light** as the **Appearance:** option when exporting.

---

### 5. **Updating the Documentation**

After saving the image, update the documentation's Markdown file, including the topology image:

```markdown
<!-- Example: ![Network Topology Diagram](../../labs_imgs/<lab-name>/<image-name>.svg) -->
