
# Minecraft Block Skin Generator

## Usage
If you need to generate an executeable, run install_program.bat. This requires [pyinstaller](https://pyinstaller.org/en/stable/index.html). The executable will be in the generated dist/ folder

The program generates the config file options.config, and the target folder generated/, where the skins are dumped when created

- 'Normal' or 'Thin' skins. These distinguish Steve vs. Alex skins (Defaults to 'Normal')

- Background color. For blocks such as leaves/ladders/etc. (Defaults to black: 000000)

- Colourizing. For dynamically coloured blocks, such as leaves and grass (Defaults to false)

- Colourization colour. Your best bet of picking a normal color is to look in your resource pack at assets/minecraft/textures/colormap.png. (No defaults, but I recommend 42b80f)

- Directory is where you can find the block's PNG file. This can be found usually in your resource pack at assets/minecraft/textures/block (Defaults to the defaultLocation property in options.config)

- Block to use. This is the name of the block texture file, so its naming may be unexpected (For example, grass_block_side). 
- - Do not include the file extention. 
- - It will accept spaces instead of underscores, and is not case sensitive. (For example, Grass Block Side, grass_block_side, and grass block side are all equivalent)


That is all! Happy generating!
