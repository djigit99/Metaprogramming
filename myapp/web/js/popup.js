p__func = $('.popup__overlay___func')
$('#popup__toggle___func').click(function() {
    p__func.css('display', 'block')
})
p__func.click(function(event) {
    e = event || window.event
    if (e.target == this) {
        $(p__func).css('display', 'none')
    }
})

p__func2 = $('.popup__overlay___func2')
$('#popup__toggle___func2').click(function() {
    p__func2.css('display', 'block')
})
p__func2.click(function(event) {
    e = event || window.event
    if (e.target == this) {
        $(p__func2).css('display', 'none')
    }
})

