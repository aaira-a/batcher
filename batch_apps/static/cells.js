$(document).ready(function(){
    $(".is_due_True.is_executed_True").addClass("green");
    $(".is_due_True.is_executed_False").addClass("red");
    $(".is_due_False.is_executed_True").addClass("yellow");
    $(".is_due_False.is_executed_False").addClass("gray");
    $(".is_due_True.is_executed_false.is_today_True").addClass("yellow");
});
