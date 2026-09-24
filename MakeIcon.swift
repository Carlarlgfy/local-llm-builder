import Cocoa
let image=NSImage(size:NSSize(width:1024,height:1024))
image.lockFocus()
NSColor(calibratedRed:0.08,green:0.12,blue:0.17,alpha:1).setFill()
NSBezierPath(roundedRect:NSRect(x:32,y:32,width:960,height:960),xRadius:200,yRadius:200).fill()
NSColor(calibratedRed:0.57,green:0.89,blue:0.75,alpha:1).setStroke()
let path=NSBezierPath();path.lineWidth=55;path.lineCapStyle = .round;path.lineJoinStyle = .round
path.move(to:NSPoint(x:340,y:665));path.line(to:NSPoint(x:195,y:510));path.line(to:NSPoint(x:340,y:355))
path.move(to:NSPoint(x:684,y:665));path.line(to:NSPoint(x:829,y:510));path.line(to:NSPoint(x:684,y:355))
path.move(to:NSPoint(x:575,y:725));path.line(to:NSPoint(x:449,y:295));path.stroke()
image.unlockFocus()
let bitmap=NSBitmapImageRep(data:image.tiffRepresentation!)!
try bitmap.representation(using:.png,properties:[:])!.write(to:URL(fileURLWithPath:CommandLine.arguments[1]))
