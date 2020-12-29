> Lackey is still being developed as a side-project.

## Introduction

Lackey bridges the gap between your code and your todos. It helps you keep track of refactoring tasks, bug fixes and other chores in your project.

## Demonstration

[DEMONSTRATION]

## Features

* Task organization - Lackey keeps your tasks categorized by task type and date
* Quick navigation - open the file with your task with quick and easy shortcuts
* Customization - if the built-in tags aren't enough, you can specify your own
* 

## Languages

The latest version of Lackey supports the following languages:

* CSS
* Deno
* Go
* HTML
* JavaScript
* Python
* Rust
* TypeScript

If there is a language or file extension you would like support for, please submit a feature request. Or, even beter, consider becoming a contributor.

## Installation

You can install Lackey like you would any other plugin, using your favorite plugin manager.

### Requirements

* Neovim
* pynvim

## Basic Usage

After you have installed Lackey, you must first initialize Lackey in the root directory of your project.

This will create a `lackey` file in your root directory. Lackey will use this directory as the starting point for collecting your tasks from your code files.

### Syntax

To find tasks, Lackey looks for certain tags in your code files. The built-in tags are:

* `FEAT` - new features
* `FIX` - bug fixes
* `DOCS` - changes or additions to documentation
* `STYLE` - formatting, indentation, naming conventions
* `REFACTOR` - review and rewrite production code
* `TEST` - writing or rewriting tests
* `TODO` - general tag for chores
* `NOTE` - general tag for comments

You might notice that these tags look like they were pulled from [Udacity's Git Commit Style Guide](https://udacity.github.io/git-styleguide/). That's because they are. Lackey also accepts user-defined tags, in case these are not to your liking or if you need even more categories.

### Single-line Tasks

By default, Lackey looks for commented lines that start with a tag that Lackey can recognize. For example, in JavaScript your code might look something like this:

```javascript
// FIX: `add` function does multiplication instead of addition
function add(a, b) {
  return a * b
}
```

Lackey only supports single line task tracking. If you need more lines to describe your task, you can add them directly into the `lackey` file.

## Commands
 
* :LackeyInit - create a `lackey` file in the current working directory
* :LackeyCollect - collect all lines and blocks that contain a Lackey tag and place them in the `lackey` file
* :LackeyShow - show all tasks
* :LackeyByTag - sort tasks by tag
* :LackeyByDate - sort tasks by date of collection
* :LackeyClean - remove finished tasks

Please refer to the [documentation]() for more information.

## Contribute

If you encounter bugs, are missing a feature, have suggestions to improve the code or other feedback, please open an issue on Github.

If you have implemented improvements to Lackey locally, please consider submitting a pull request.

## License

[The MIT License](https://raw.githubusercontent.com/heyitschun/vim-lackey/master/LICENSE) © [Chun Poon](https://heyitschun.com)
