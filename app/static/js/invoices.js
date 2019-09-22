function createTb(server) {

    $("#jsGrid").jsGrid({
        width: "100%",
        height: "900px",
        heading: true,
        paging: true,
        pageSize: 20,
        pagePrevText: "назад",
        pageNextText: "вперед",
        pageFirstText: "начало",
        pageLastText: "конец",
        pagerFormat: "Страницы: {first} {prev} {pages} {next} {last}    {pageIndex} из {pageCount}",
        pageNavigatorNextText: "...",
        pageNavigatorPrevText: "...",
        deleteConfirm: "Удаление! Вы уверенны?",

        controller: {
            loadData: function(filter) {
                
            },
            updateItem: function(item) {
                item.rowid = item.CustomerId;
                return $.ajax({
                    type: "PUT",
                    url: "/crud/chinook/invoices",
                    data: item,
                });
            },
            insertItem: function(item) {
                item.rowid = item.CustomerId;
                return $.ajax({
                    type: "POST",
                    url: "/crud/chinook/invoices",
                    data: item,
                });
            },
           deleteItem: function(item) {
            item.rowid = item.CustomerId;
                $.ajax({
                    type: "DELETE",
                    url: "/crud/chinook/invoices",
                    data: item
                });
            },

        },
        data : server,
        fields: [
            { name: "rowid", type: "number", width: 40, visible:false},
            { name: "InvoiceId", title:"id", type: "number", width: 35},
            { name: "CustomerId", title:"CID",type: "textarea", width: 30},
            { name: "InvoiceDate", type: "text", width: 80},
            { name: "BillingAddress", title:"Address",type: "text", width: 90, visible:true},
            { name: "BillingCity", type: "text", width: 70},
            { name: "BillingState", title:"STATE", type: "text", width: 40 },
            { name: "BillingPostalCode",title:"CODE", type: "text", width: 30 },
            { name: "Total", type: "text", width: 40 },
        ]
    });
}

var dataServer = null;

$.ajax({
    url: "/crud/chinook/invoices?method=get_rows",
    dataType: "json",
  }).done(function(data){
      dataServer = data;
      createTb(data);
  })