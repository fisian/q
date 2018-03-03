This is a test to show function redefinition
q qqqqqqq function 7
    qqqqqqqq qqqqqqqqqqqqqqqqqq qqqq qqqqqqqq qqqq qqq qqqq qqq qqq q qqqq qqqq qqq q print '7:' to identify function
    q qqqq function 7.4
        qqqqqqqq qqqqqqqqqqqqqqqqqq qqqq qqq qqqqqqqq qqqqqqqqqqqqqqqq qqqq qqqqqqqq qqqq qqqqq qqqq qqq qqq q qqqq qqqq qqq q print '7.2:' to identify function
        qqqq qqqq qqq q print from stack
    qq qqqq f7.4 end
    qqq q exec f7.4
qq qqqqqqq
qqqq qq qqq q pop function id
q qq function 2
    qqqqqqqq qqqqqqqqqqqqqqqqqq qqqq qqq qqqq qqq qqqq qqq qqq q qqqq qqqq qqq q print '2:' to identify function
    q qqq function 2.3
        qqqqqqqq qqqqqqqqqqqqqqqqqq qqqq qqqq qqqqqqqq qqqqqqqqqqqqqqqq qqqq qqq qqqq qqqqq qqqq qqq qqq q qqqq qqqq qqq q print '2.3:' to identify function
        qqqq qqqq qqq q print from stack
    qq qqq f2.3 end
    qqq q exec f2.3
qq qq f2 end
qqqq qq qqq q pop function id
q qqqqq function 5: push 'Hello world!'
    qqqqqqqq qq ! qqqqqq qqqq d qqqqqq qqqqqqqqqqqq l qqqqqq qqqqqqqqqqqqqqqqqq r qqqqqq qqqqqqqqqqqqqqq o qqqqqq qqqqqqqqqqqqqqqqqqqqqqq w qqqqqqqq q SPACE
    qqqqqq qqqqqqqqqqqqqqq o qqqqqq qqqqqqqqqqqq l qqqqqq qqqqqqqqqqqq l qqqqqq qqqqq e qqqqqqq qqqqqqqq H
    qqqq qqqqqqqqqqqqq qqqq qqq qqq q make_string(13)
qq qqqqq f5 end
qqq q exec f5
qqqqq qqqqqq qqq q exec f5
qqqqq qqqqqq qqq q exec f5
Here the stack looks like this: ['Hello world!', Hello world!', 'Hello world!']
qqqqq qqq qqq q exec f2
qqqqq qqqqqqqq qqq q exec f6
qqqqq qqqqq qqq q exec f4
