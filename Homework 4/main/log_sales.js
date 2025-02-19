const salesperson = "Lindsey Rosales - Best TA and Datadog SWE";
let salesData = [
	{
		"salesperson": "James D. Halpert",
		"client": "Shake Shack",
		"reams": 100
	},
	{
		"salesperson": "Stanley Hudson",
		"client": "Toast",
		"reams": 400
	},
	{
		"salesperson": "Michael G. Scott",
		"client": "Computer Science Department",
		"reams": 1000
	},
]
let clients = [
    "Shake Shack",
    "Toast",
    "Computer Science Department",
    "Teacher's College",
    "Starbucks",
    "Subsconsious",
    "Flat Top",
    "Joe's Coffee",
    "Max Caffe",
    "Nussbaum & Wu",
    "Taco Bell",
];

$(document).ready(function() {
    $("#client").autocomplete({
        source: clients
    });

    $("#submit-sale").click(addSale);
    $("#reams").keypress(function(event) {
        if (event.key === "Enter") {
            addSale();
        }
    });
    loadScreen();
});

function addSale() {
    const client = $("#client").val().trim();
    const reams = $("#reams").val().trim();

    if ($("#reams-warning").length === 0) {
        $("#reams").after("<span id='reams-warning' class='text-danger'></span>");
    }
    if ($("#client-warning").length === 0) {
        $("#client").after("<span id='client-warning' class='text-danger'></span>");
    }

    $("#client-warning").text("").hide();
    $("#reams-warning").text("").hide();

    if (!client) {
        $("#client-warning").text("Client name is required.").show();
        $("#client").focus();
        return;
    }

    if (!reams) {
        $("#reams-warning").text("Number of reams is required.").show();
        $("#reams").focus();
        return;
    }

    if (!/^[0-9]+$/.test(reams)) {
        $("#reams-warning").text("Valid number of reams is required.").show();
        $("#reams").focus();
        return;
    }

    if (!clients.includes(client)) {
        clients.push(client);
    }

    salesData.unshift({ client, reams, salesperson });

    renderSales();

    $("#client, #reams").val("");
    $("#client").focus();
    $("#client-warning, #reams-warning").hide();
}

function renderSales() {
    const salesContainer = $("#sales-records");
    salesContainer.empty();
    salesData.forEach((sale, index) => {
        const saleRow = $(`
            <div class='d-flex flex-column border p-3 mt-2 sale-row' draggable='true' ondragstart='drag(event, ${index})' style='cursor: move; width: 100%;'>
                <span><strong>${sale.salesperson}</strong></span>
                <span>Client: ${sale.client}</span>
                <span>Reams: ${sale.reams}</span>
                <button class='btn btn-danger btn-sm mt-2 delete-btn' onclick='deleteSale(${index})'>X</button>
            </div>
        `);
        salesContainer.append(saleRow);
    });

    $(".sale-row").hover(
        function() {
            $(this).css("background-color", "lightyellow");
        }, 
        function() {
            $(this).css("background-color", "");
        }
    );
}

function deleteSale(index) {
    salesData.splice(index, 1);
    renderSales();
}

function drag(event, index) {
    event.dataTransfer.setData("text", index);
}

$("#trash").on("dragover", function(event) {
    event.preventDefault();
    $(this).addClass("bg-warning");
    $(this).css("cursor", "grabbing");
});

$("#trash").on("dragleave", function() {
    $(this).removeClass("bg-warning");
    $(this).css("cursor", "default");
});

$("#trash").on("drop", function(event) {
    event.preventDefault();
    const index = event.originalEvent.dataTransfer.getData("text");
    deleteSale(index);
    $(this).removeClass("bg-warning");
    $(this).css("cursor", "default");
});

function loadScreen() { 
    renderSales();
}
