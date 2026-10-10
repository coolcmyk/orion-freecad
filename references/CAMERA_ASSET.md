# Waveshare RPi Camera (G) reference search

Confirmed identity: OV5647, 5 MP, 160-degree diagonal field of view, 25 × 24 mm PCB. User supplied the Tokopedia Arduino Store listing and product image; these do not establish lens depth or populated board thickness.

- Official product: https://www.waveshare.com/product/rpi-camera-g.htm
- Official resources: https://www.waveshare.com/wiki/RPi_Camera_(G)
- Mechanical archive: https://www.waveshare.com/w/upload/8/8a/RPi_Camera_E_F_G_H_Mechanical.zip
- Saved archive: `RPi_Camera_E_F_G_H_Mechanical.zip`; extracted drawing: `camera_mechanical/RPi_Camera_E_F_G_H_Mechanical.dwg`. The archive contains one DWG and no 3D STEP file.
- Also inspected the official pan-tilt STEP archive: https://files.waveshare.com/wiki/2-Axis-Pan-Tilt-Camera-Module/2-Axis_Pan-Tilt_Camera_Module_STEP.zip
- Saved as `Waveshare_Pan_Tilt_STEP.zip`. Its `PT v6.step` identifies camera products as `rpiCameraM` and `rpiCameraM_lens`. It was not imported into ORION as an exact Type G reference.

No verified exact manufacturer Type G 3D asset was found in the inspected resources. A native reconstruction is now saved in `camera_g_reconstructed/Waveshare_Camera_G.FCStd`, with a STEP export and provenance record. It uses the decoded DWG board/hole geometry and explicitly provisional lens/depth/connector parameters. ORION includes that reconstruction. Lens diameter/depth, rear components, connector geometry and cable bend allowance still need actual measurements or matching manufacturer CAD. The photographed protective cap is not a measured operating-lens envelope.
