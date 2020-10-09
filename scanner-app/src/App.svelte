<script>
  import Quagga from "quagga";

  let scannerRef;
  let isRunning = false;

  function startScanner() {
    Quagga.init(
      {
        inputStream: {
          name: "Live",
          type: "LiveStream",
          target: scannerRef,
          constraints: {
            width: 480,
            height: 320,
            facingMode: "environment",
          },
        },
        decoder: {
          readers: ["upc_reader", "upc_e_reader"],
          debug: {
            showCanvas: true,
            showPatches: true,
            showFoundPatches: true,
            showSkeleton: true,
            showLabels: true,
            showPatchLabels: true,
            showRemainingPatchLabels: true,
            boxFromPatches: {
              showTransformed: true,
              showTransformedBox: true,
              showBB: true,
            },
          },
        },
      },
      (err) => {
        if (err) {
          alert.log(err);
          return;
        }

        Quagga.start();
        isRunning = true;
      }
    );

    Quagga.onProcessed((result) => {
      var drawingCtx = Quagga.canvas.ctx.overlay,
        drawingCanvas = Quagga.canvas.dom.overlay;

      if (result) {
        if (result.boxes) {
          drawingCtx.clearRect(
            0,
            0,
            parseInt(drawingCanvas.getAttribute("width")),
            parseInt(drawingCanvas.getAttribute("height"))
          );
          result.boxes
            .filter((box) => {
              return box !== result.box;
            })
            .forEach((box) => {
              Quagga.ImageDebug.drawPath(box, { x: 0, y: 1 }, drawingCtx, {
                color: "green",
                lineWidth: 2,
              });
            });
        }

        if (result.box) {
          Quagga.ImageDebug.drawPath(result.box, { x: 0, y: 1 }, drawingCtx, {
            color: "#00F",
            lineWidth: 2,
          });
        }

        if (result.codeResult && result.codeResult.code) {
          Quagga.ImageDebug.drawPath(
            result.line,
            { x: "x", y: "y" },
            drawingCtx,
            { color: "red", lineWidth: 3 }
          );
        }
      }
    });

    Quagga.onDetected((result) => {
      console.log(
        "Barcode detected and processed : [" + result.codeResult.code + "]",
        result
      );
    });
  }

  let products = [
    { name: "	Thatchers Gold Cider 500ml" },
    { name: "more booze" },
    { name: "extra booze" },
  ];

  let d = new Date();
  let when = d.toUTCString();

  //* Scanner file: Date, Time, Qty, barcode
  // 18/07/20,13:06:08,01,5060391623825
  // 18/07/20,13:06:13,01,5060391623825
  // 18/07/20,13:06:16,01,5060391623825
  // 18/07/20,13:07:21,01,5034660021582
  // 18/07/20,13:07:26,01,50184453
  // 18/07/20,13:07:36,01,20453756
  // 18/07/20,13:07:49,01,5010421073502
  // 18/07/20,13:07:54,01,5010421073793
  // 18/07/20,13:08:00,01,5010421073755

  // newline is %0D%0A

  let file =
    "18/07/20,13:06:08,01,5060391623825%0D%0A18/07/20,13:06:13,01,5060391623825";
</script>

<main role="main" class="flex-shrink-0">
  <div class="container">
    <h1 class="mt-5">⚡ Sammy Scanner</h1>
    <p class="lead">The free mobile scanner for Booker customers</p>
    <p>
      Think you need to buy an expensive scannner for stock takes and purchase
      orders ? Think again. Sammy Scanner allows you to scan all product
      barcodes and record the quantity. It can then save a generated file that
      you can a upload to Booker to create a shopping list or import it into
      Excel to do stock takes.
    </p>
    <div bind:this={scannerRef} />

    <div
      class="btn-toolbar mb-3"
      role="toolbar"
      aria-label="Toolbar with button groups">
      <button
        type="button"
        class="btn btn-primary mr-2"
        on:click={() => (isRunning ? Quagga.stop() : startScanner())}>
        Toggle Scanner
      </button>

      <form
        action="mailto:your email?subject=Sammy Scanner File ({when})&body={file}"
        method="post"
        class="mr-2">
        <button type="submit" class="btn btn-primary">Email File</button>
      </form>

      <form
        action="https://www.booker.co.uk/catalog/scanneruploadcs3000.aspx"
        target="_blank"
        class="mr-2">
        <input class="btn btn-secondary" type="submit" value="Upload" />
      </form>
    </div>
    <table class="table mt-5">
      <thead>
        <tr>
          <th scope="col">Image</th>
          <th scope="col">Name</th>
          <th scope="col">Quantity</th>
          <th scope="col">Barcode</th>
          <th scope="col">Code</th>
        </tr>
      </thead>
      <tbody>
        {#each products as { name }}
          <tr>
            <td>
              <img
                src="https://www.booker.co.uk/bbimages/1/32185ae4-aeb8-4b56-be18-68c1c61b421c.jpg"
                style="width: 1.5rem"
                alt />
            </td>
            <td>{name}</td>
            <td>3</td>
            <td>000000000</td>
            <td>197908</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</main>
