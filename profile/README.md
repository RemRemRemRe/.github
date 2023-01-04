Hi there, thanks for taking a look at this.
Here are my coding toys that I build up on my spare time.

# Reminder
These codes are pretty experiemental for now, things may change dramaticly at any time
I wrote them with ue5-main branch only, and did not do testing or packaging or something like that

## Cpp version
c++ 17 or newer is required

So, keep that in mind🤗. 

# Module shared right now
- [Common](https://github.com/RemRemRemRe/Common.git)
- [MyBlank](https://github.com/RemRemRemRe/MyBlank.git)
- [DetailCustomizationUtilities](https://github.com/RemRemRemRe/DetailCustomizationUtilities.git)
- [WidgetComponent](https://github.com/RemRemRemRe/WidgetComponent.git)
- [WidgetComponentEditor](https://github.com/RemRemRemRe/WidgetComponentEditor.git)

# My `.gitmodules` config
If you want to try it out, consider add these to your `.gitmodules` file

```ini
[submodule "Plugins/GameFeatures/Editor/DetailCustomizationUtilities"]
	path = Plugins/GameFeatures/Editor/DetailCustomizationUtilities
	url = https://github.com/RemRemRemRe/DetailCustomizationUtilities.git
[submodule "Plugins/GameFeatures/Editor/MyBlank"]
	path = Plugins/GameFeatures/Editor/MyBlank
	url = https://github.com/RemRemRemRe/MyBlank.git
[submodule "Plugins/GameFeatures/Editor/WidgetComponentEditor"]
	path = Plugins/GameFeatures/Editor/WidgetComponentEditor
	url = https://github.com/RemRemRemRe/WidgetComponentEditor.git

[submodule "Plugins/GameFeatures/Runtime/UMG/WidgetComponent"]
	path = Plugins/GameFeatures/Runtime/UMG/WidgetComponent
	url = https://github.com/RemRemRemRe/WidgetComponent.git
[submodule "Plugins/GameFeatures/Runtime/Utilities/Common"]
	path = Plugins/GameFeatures/Runtime/Utilities/Common
	url = https://github.com/RemRemRemRe/Common.git
```

# A bit about myself
I start to actually work with unreal for about 3 years now (5/15/2022) and hoping to become more experienced with Unreal and C++.

I remmerber when I started my unreal source code journey as an intern, I made a real mess on `PerforceSourceControlModule` (and the engine).

Tell you a horrible story : 
In order to do something i can't recall now, I tried to move all the code of `ContentBrowser` module from `Private` folder to `Public`🤣

So i decided to focus on `gameplay` now (doge)

# Advice is appreciated
Any advice about what I wrote or going to write is welcomed, and hopefully there would be many issues and pull requests come in😊.

# Have a nice day 🍀

# Credits ♥
![JetBrains Logo (Main) logo](https://resources.jetbrains.com/storage/products/company/brand/logos/jb_beam.svg)
https://jb.gg/OpenSourceSupport