var em;
$(function () {
  var total = 0.0;


  var arrayLength = em.length;
    // function to shift elements from the Employee list to the PO List
    $("#btn1").click(function (){

      $("#emplist option:selected").each(function (){
        $(this).remove().appendTo("#polist");
        //added by shivangi to calculate total rate
        console.log(this);

        for (var i = 0; i < arrayLength; i++)
        {

           console.log("Inside for loop :::");
           console.log("Employee name is :"+em[i][1]);
           console.log("Employee name moved to PO list is :"+this.value);
           if(em[i][1] == this.value)
           {
             console.log("Selected value matched ! Inside if block");
             console.log("Employee rate is : "+em[i][2]);
             total +=  em[i][2];
             $("#rateWithoutGST").val(total);
            $("#rateWithGST").val(total+(0.18*total));
             break;
           }

         }
  console.log("total rate of PO is "+total);


      });


      });
    // function to shift elements from the PO List to Employee List
    $("#btn2").click(function (){
      $("#polist option:selected").each(function (){
        $(this).remove().appendTo("#emplist");
        // Added by Shivangi
        for (var i = 0; i < arrayLength; i++)
        {

           console.log("Inside for loop :: ");
           console.log("Employee name is :"+em[i][1]);
           console.log("Employee name moved to PO list is :"+this.value);
           if(em[i][1] == this.value)
           {
            console.log("Selected value matched ! Inside if block");
            console.log("Employee rate is : "+em[i][2]);

            total -=  em[i][2];
            $("#rateWithoutGST").val(total);
            $("#rateWithGST").val(total+(0.18*total));
            break;
           }

         }
         console.log("Total value after subtracting from PO list : "+total);
      });
    });
});

function EmpData(vars)
{
  em = vars;

}
