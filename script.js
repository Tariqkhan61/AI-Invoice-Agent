// ===============================
// AI INVOICE AGENT
// ===============================

const invoiceForm = document.getElementById("invoiceForm");

invoiceForm.addEventListener("submit", function (event) {

    // Page refresh ko rokna
    event.preventDefault();

    // ===============================
    // FORM VALUES
    // ===============================

    const customerName =
        document.getElementById("customerName").value.trim();

    const customerEmail =
        document.getElementById("customerEmail").value.trim();

    const productName =
        document.getElementById("productName").value.trim();

    const quantity =
        Number(document.getElementById("quantity").value);

    const price =
        Number(document.getElementById("price").value);

    const discount =
        Number(document.getElementById("discount").value) || 0;


    // ===============================
    // VALIDATION
    // ===============================

    if (
        !customerName ||
        !productName ||
        quantity <= 0 ||
        price < 0
    ) {
        alert("Please enter valid invoice information.");
        return;
    }


    // ===============================
    // CALCULATIONS
    // ===============================

    const subtotal = quantity * price;

    const total = Math.max(
        subtotal - discount,
        0
    );


    // ===============================
    // INVOICE NUMBER
    // ===============================

    const invoiceNumber =
        "INV-" + Date.now().toString().slice(-6);


    // ===============================
    // DATE
    // ===============================

    const invoiceDate =
        new Date().toLocaleDateString();


    // ===============================
    // UPDATE INVOICE PREVIEW
    // ===============================

    document.getElementById("previewInvoiceNumber").textContent =
        invoiceNumber;

    document.getElementById("previewDate").textContent =
        invoiceDate;

    document.getElementById("previewCustomer").textContent =
        customerName;

    document.getElementById("previewEmail").textContent =
        customerEmail || "Email not provided";

    document.getElementById("previewProduct").textContent =
        productName;

    document.getElementById("previewQuantity").textContent =
        quantity;

    document.getElementById("previewItemTotal").textContent =
        "PKR " + subtotal.toLocaleString();

    document.getElementById("previewSubtotal").textContent =
        "PKR " + subtotal.toLocaleString();

    document.getElementById("previewDiscount").textContent =
        "PKR " + discount.toLocaleString();

    document.getElementById("previewTotal").textContent =
        "PKR " + total.toLocaleString();


    // ===============================
    // SHOW INVOICE PREVIEW
    // ===============================

    const invoicePreview =
        document.getElementById("invoicePreview");

    invoicePreview.style.display = "block";


    // Smoothly scroll to invoice
    invoicePreview.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });


    // ===============================
    // SEND DATA TO PYTHON BACKEND
    // ===============================

    sendInvoiceToPython({
        customerName: customerName,
        customerEmail: customerEmail,
        productName: productName,
        quantity: quantity,
        price: price,
        discount: discount
    });

});


// ===============================
// DOWNLOAD PDF
// ===============================

const downloadPdfBtn =
    document.getElementById("downloadPdfBtn");

downloadPdfBtn.addEventListener("click", function () {

    // Check jsPDF
    if (!window.jspdf) {
        alert("PDF library is not loaded. Please refresh the page.");
        return;
    }

    const { jsPDF } = window.jspdf;

    // Create PDF
    const pdf = new jsPDF();


    // ===============================
    // GET INVOICE INFORMATION
    // ===============================

    const invoiceNumber =
        document.getElementById("previewInvoiceNumber").textContent;

    const invoiceDate =
        document.getElementById("previewDate").textContent;

    const customer =
        document.getElementById("previewCustomer").textContent;

    const email =
        document.getElementById("previewEmail").textContent;

    const product =
        document.getElementById("previewProduct").textContent;

    const quantity =
        document.getElementById("previewQuantity").textContent;

    const itemTotal =
        document.getElementById("previewItemTotal").textContent;

    const subtotal =
        document.getElementById("previewSubtotal").textContent;

    const discount =
        document.getElementById("previewDiscount").textContent;

    const total =
        document.getElementById("previewTotal").textContent;


    // ===============================
    // PDF HEADER
    // ===============================

    pdf.setFontSize(22);
    pdf.setFont("helvetica", "bold");

    pdf.text(
        "AI INVOICE AGENT",
        20,
        25
    );

    pdf.setFontSize(11);
    pdf.setFont("helvetica", "normal");

    pdf.text(
        "Muhammad Tariq Mahboob",
        20,
        33
    );

    pdf.line(
        20,
        40,
        190,
        40
    );


    // ===============================
    // INVOICE INFORMATION
    // ===============================

    pdf.setFontSize(11);

    pdf.text(
        "Invoice No: " + invoiceNumber,
        20,
        52
    );

    pdf.text(
        "Date: " + invoiceDate,
        20,
        60
    );


    // ===============================
    // CUSTOMER
    // ===============================

    pdf.setFont("helvetica", "bold");

    pdf.text(
        "BILL TO",
        20,
        75
    );

    pdf.setFont("helvetica", "normal");

    pdf.text(
        customer,
        20,
        83
    );

    pdf.text(
        email,
        20,
        91
    );


    // ===============================
    // ITEM
    // ===============================

    pdf.setFont("helvetica", "bold");

    pdf.text(
        "DESCRIPTION",
        20,
        108
    );

    pdf.text(
        "QTY",
        125,
        108
    );

    pdf.text(
        "AMOUNT",
        155,
        108
    );

    pdf.line(
        20,
        112,
        190,
        112
    );

    pdf.setFont("helvetica", "normal");

    pdf.text(
        product,
        20,
        122
    );

    pdf.text(
        quantity,
        125,
        122
    );

    pdf.text(
        itemTotal,
        155,
        122
    );


    // ===============================
    // SUMMARY
    // ===============================

    pdf.line(
        20,
        135,
        190,
        135
    );

    pdf.text(
        "Subtotal:",
        125,
        147
    );

    pdf.text(
        subtotal,
        160,
        147
    );

    pdf.text(
        "Discount:",
        125,
        157
    );

    pdf.text(
        discount,
        160,
        157
    );

    pdf.setFont("helvetica", "bold");

    pdf.setFontSize(14);

    pdf.text(
        "TOTAL:",
        125,
        172
    );

    pdf.text(
        total,
        160,
        172
    );


    // ===============================
    // FOOTER
    // ===============================

    pdf.setFontSize(10);

    pdf.setFont("helvetica", "normal");

    pdf.text(
        "Generated by AI Invoice Agent",
        20,
        260
    );

    pdf.text(
        "Muhammad Tariq Mahboob",
        20,
        268
    );

    pdf.text(
        "Powered by Python + AI",
        20,
        276
    );


    // ===============================
    // SAVE PDF
    // ===============================

    pdf.save(
        invoiceNumber + ".pdf"
    );

});


// ===============================
// CONNECT TO PYTHON BACKEND
// ===============================

async function sendInvoiceToPython(invoiceData) {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/create-invoice",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(invoiceData)
            }
        );


        // Python response
        const result = await response.json();
        console.log("GEMINI SUMMARY:", result.invoice.aiSummary);
        // Show Gemini AI Summary on website
const aiSummaryElement = document.getElementById("aiSummary");

if (aiSummaryElement && result.invoice && result.invoice.aiSummary) {
    aiSummaryElement.textContent = result.invoice.aiSummary;
}

        console.log(
            "Python Backend Response:",
            result
        );


        if (result.success) {

            console.log(
                "✅ Invoice successfully sent to Python!"
            );

        } else {

            console.error(
                "❌ Python backend returned an error."
            );

        }

    } catch (error) {

        console.error(
            "❌ Cannot connect to Python backend:",
            error
        );

    }

}