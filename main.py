from PIL import Image
import time

def ShrinkNumber(Number):
    # converts a number like 135 to "0.529"
    return Number / 255 == 1 and "1" or Number / 255 == 0 and "0" or str(Number / 255)[:5]

def ValuesToPixelArray(Values):
    # f'{ R }, { G }, { B }, { A or 1 }'
    return f'{ShrinkNumber(Values[0])}, {ShrinkNumber(Values[1])}, {ShrinkNumber(Values[2])}, {len(Values) == 4 and ShrinkNumber(Values[3]) or "1"}'

StartTime = time.time()

ImagePath = 'Image.png'
XMLPath = 'Result.rbxmx'

Img = Image.open(ImagePath)

# because the maximum size is 1024x1024
# example: 1920x1080 becomes 1024x576
if Img.size[0] > Img.size[1] and Img.size[0] > 1024:
    NewSize = int((Img.size[1] / Img.size[0]) * 1024)
    Img = Img.resize((1024, NewSize))
elif Img.size[1] > Img.size[0] and Img.size[1] > 1024:
    NewSize = int((Img.size[0] / Img.size[1]) * 1024)
    Img = Img.resize((NewSize, 1024))

Picture = Img.load()

with open(XMLPath, "w") as File:
    #clean the XML file
    File.write("")
    File.close()

# open the XML
XMLFile = open(XMLPath, "a")
XMLFile.write("""<roblox xmlns:xmime="http://www.w3.org/2005/05/xmlmime" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.roblox.com/roblox.xsd" version="4">
	<Meta name="ExplicitAutoJoints">true</Meta>
	<External>null</External>
	<External>nil</External>
	<Item class="ModuleScript" referent="RBXA66C2A12C59C455E92E25C20A400D5AE">
		<Properties>
			<BinaryString name="AttributesSerialize"></BinaryString>
			<SecurityCapabilities name="Capabilities">0</SecurityCapabilities>
			<bool name="DefinesCapabilities">false</bool>
			<Content name="LinkedSource"><null></null></Content>
			<string name="Name">ImageResult</string>
			<string name="ScriptGuid">{47B60619-4224-41F2-82C1-3B8ED8773817}</string>
			<ProtectedString name="Source"><![CDATA[""")

Width, Height = Img.size
PixelsAmount = (Width * Height)

XMLFile.write("""return {\n	["Resolution"] = Vector2.new(""" + str(Width) + """, """ + str(Height) + """),\n	["Image"] = {""")
# set up the module script's source

Percent = -1
Pixel = 0

for Y in range(Height):
    XMLFile.write("\n		")

    for X in range(Width):
        Pixel += 1
        NewPercent = int(Pixel / PixelsAmount * 100)
        
        if Percent < NewPercent:
            print(str(NewPercent) + "%	pixels: " + str(Pixel))
            Percent = NewPercent

        XMLFile.write(ValuesToPixelArray(Picture[X, Y]) + ", ")

# close the module script
XMLFile.write("""\n	}\n}]]></ProtectedString>
            <int64 name="SourceAssetId">-1</int64>
            <BinaryString name="Tags"></BinaryString>
        </Properties>
    </Item>
</roblox>""")
XMLFile.close()

print("TIME TOOK: " + str(time.time() - StartTime))
print("PRESS ESC TO EXIT")

import keyboard
keyboard.wait("esc")
