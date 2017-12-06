import sublime
import sublime_plugin

class PasteWithTabCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        clipboardStr = sublime.get_clipboard()
        clipboardStr = clipboardStr.expandtabs(4)
        split_symbol = '\n'
        if clipboardStr.find('\r\n') > -1:
            split_symbol = '\r\n'
        s_list = clipboardStr.split(split_symbol)
        preIndent = 0
        if len(s_list) == 1:
            self.view.run_command('paste_and_indent')
        else:
            preIndent = self.getLeftSpace(s_list[0])
            if preIndent == 0:
                preIndent = 1000
            leftSpaceList = [0]
            for s in s_list[1:]:
                leftSpace = self.getLeftSpace(s)
                leftSpaceList.append(leftSpace)
                preIndent = leftSpace if leftSpace < preIndent else preIndent
            s_list[0] = s_list[0].lstrip()
            minPreIndentSpace = 1000
            leftSpaceList.sort()
            for i in range(1, len(leftSpaceList)):
                leftSpaceSplit = leftSpaceList[i] - leftSpaceList[i-1]
                if leftSpaceSplit > 0 and leftSpaceSplit < minPreIndentSpace:
                    minPreIndentSpace = leftSpaceSplit
            if preIndent > 0:
                for index in range(1, len(s_list)):
                    s = s_list[index]
                    if self.getLeftSpace(s) >= preIndent and len(s.strip()) > 0:
                        s_list[index] = s[preIndent:]
            if minPreIndentSpace == 2:
                for index in range(0, len(s_list)):
                    if self.getLeftSpace(s_list[index]) >= minPreIndentSpace:
                        s_list[index] = s_list[index].replace('  ', '    ')
            clipboardStr = split_symbol.join(s_list)
            sublime.set_clipboard(clipboardStr)
            self.view.run_command('paste_and_indent')

    def getLeftSpace(self, s):
        return len(s) - len(s.lstrip())
