Note:
Do not replace 
⸺+\n
with
------------------------------------------------------------------------\n
in original vocab_book.txt
as ⸺+\n will always be appended to the original file.

可能的问题：
========================================================================
☣ ERROR: 解析daemon返回结果失败: unexpected end of JSON input
这在更新了bash脚本能够append输入值之后应该已经不会再出现了。

注意，python脚本不能解决这个问题，因为python只会保留第一次查询的记录。
我希望修改一下python脚本，让它更新为最后一次查询的记录，可能就能解决这个问题。
