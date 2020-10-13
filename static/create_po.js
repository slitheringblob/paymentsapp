$(function () {
    // function to shift elements from the Employee list to the PO List
    $("#btn1").click(function (){
      $("#emplist option:selected").each(function (){
        $(this).remove().appendTo("#polist");
      });
    });
    // function to shift elements from the PO List to Employee List
    $("#btn2").click(function (){
      $("#polist option:selected").each(function (){
        $(this).remove().appendTo("#emplist");
      });
    });
});
