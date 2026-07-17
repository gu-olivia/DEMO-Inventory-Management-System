console.log("app.js loaded");

window.editing = {
  type: null,
  id: null,
};

window.deleteProduct = async function (product_id) {
  console.log("clicked", product_id);

  if (!confirm("Delete this product?")) return;

  let response = await fetch(`/api/products/${product_id}`, {
    method: "DELETE",
  });

  console.log("status:", response.status);

  loadProducts();
};

async function loadProducts() {
  let response = await fetch("/api/products");
  let data = await response.json();

  let tableBody = document.getElementById("productsTable");

  tableBody.innerHTML = "";
  data.forEach((product) => {
    tableBody.innerHTML += `
            <tr>
                <td>${product.product_id}</td>
                <td>${product.product_name}</td>
                <td>${product.ab_name}</td>
                <td>${product.fluorophore_id}</td>
                <td>${product.fluorophore_name}</td>
                <td>${product.host_isotype_name}</td>
                <td>${product.part_number}</td>
                <td>${product.clone_name}</td>
                <td>${product.product_category}</td>
                <td>${product.top_products}</td>
                <td>
                <button onclick="updateProduct(${product.product_id})">
                    Edit
                </button>
            </td>
                <td>
                <button onclick="deleteProduct(${product.product_id})">
                    Delete
                </button>
            </td>
            </tr>

        `;
  });
}
document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("productsTable")) {
    loadProducts();
  }
});

async function loadLots() {
  try {
    let response = await fetch("/api/lots");

    let data = await response.json();
    let tableBody = document.getElementById("lotsTable");

    tableBody.innerHTML = "";
    data.forEach((lot) => {
      tableBody.innerHTML += `
                <tr>
                    <td>${lot.lot_id}</td>
                    <td>${lot.product_id}</td>
                    <td>${lot.lot_number}</td>
                    <td>${lot.creation_date}</td>
                    <td>${lot.expiration_date}</td>
                    <td>${lot.product_state}</td>
                    <td>${lot.test_5uL_concentration_ug_ml}</td>
                    <td>${lot.initial_volume_ml}</td>
                    <td>${lot.remarks}</td>
                        <td>
                    <button onclick="updateLot(${lot.lot_id})">
                        Edit
                    </button>
                </td>
                    <td>
                    <button onclick="deleteLot(${lot.lot_id})">
                        Delete
                    </button>
                </td>
                </tr>
            `;
    });
  } catch (error) {
    console.error("Could not load lots:", error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("lotsTable")) {
    loadLots();
  }
});

async function loadBulkInventory() {
  try {
    let response = await fetch("/api/bulk_inventory");
    console.log("Response status:", response.status);
    let data = await response.json();
    console.log("JSON:", data);
    let tableBody = document.getElementById("bulkTable");
    tableBody.innerHTML = "";
    data.forEach((bulk_product) => {
      let row = `
        <tr>
          <td>${bulk_product.product_name}</td>
          <td>${bulk_product.ab_name}</td>
          <td>${bulk_product.fluorophore_name}</td>
          <td>${bulk_product.host_isotype_name}</td>
          <td>${bulk_product.part_number}</td>
          <td>${bulk_product.clone_name}</td>
          <td>${bulk_product.lot_number}</td>
          <td>${bulk_product.creation_date}</td>
          <td>${bulk_product.expiration_date}</td>
          <td>${bulk_product.initial_volume_mk}</td>
          <td>${bulk_product.current_volume_ml}</td>
          <td>${bulk_product.storage_concentration_ug_mL}</td>
          <td>${bulk_product.location}</td>
          <td>${bulk_product.buffer}</td>
          <td>${bulk_product.remarks}</td>
          <td>${bulk_product.top_products}</td><td>
                          <button onclick="updateBulkProduct(${bulk_product.lot_id})">
                    Edit
                </button>
            </td>
                <td>
                <button onclick="deleteBulkProduct(${bulk_product.lot_id})">
                    Delete
                </button>
        </tr>
      `;

      tableBody.innerHTML += row;
    });
  } catch (error) {
    console.error("Could not load bulk inventory:", error);
  }
}

document.addEventListener("DOMContentLoaded", loadBulkInventory);

async function loadPackagedInventory() {
  try {
    let response = await fetch("/api/packaged_inventory");
    console.log("Response status:", response.status);
    let data = await response.json();
    console.log("JSON:", data);
    let tableBody = document.getElementById("packagedTable");
    tableBody.innerHTML = "";
    console.log("Empty Packaged table loaded!");
    data.forEach((packaged_product) => {
      let row = `
        <tr>
          <td>${packaged_product.product_catalog_number}</td>
          <td>${packaged_product.unit_price}</td>
          <td>${packaged_product.product_name}</td>
          <td>${packaged_product.clone_name}</td>
          <td>${packaged_product.size}</td>
          <td>${packaged_product.lot_number}</td>
          <td>${packaged_product.packaging_date}</td>
          <td>${packaged_product.packaging_concentration_ug_mL}</td>
          <td>${packaged_product.location}</td>
          <td>${packaged_product.qty_remaining}</td>
          <td>${packaged_product.buffer}</td>
          <td>${packaged_product.cost_of_goods}</td>
          <td>${packaged_product.remarks}</td><td>
                          <button onclick="updatePackagedProduct(${packaged_product.packaged_id})">
                    Edit
                </button>
            </td>
                <td>
                <button onclick="deletePackagedProduct(${packaged_product.packaged_id})">
                    Delete
                </button>
        </tr>
      `;

      tableBody.innerHTML += row;
    });
  } catch (error) {
    console.error("Could not load bulk inventory:", error);
  }
}

document.addEventListener("DOMContentLoaded", loadPackagedInventory);

const productForm = document.getElementById("productForm");

if (productForm) {
  productForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    let product = {
      product_name: document.getElementById("product_name").value,
      ab_name: document.getElementById("ab_name").value,
      fluorophore_name: document.getElementById("fluorophore_name").value,
      host_isotype_name: document.getElementById("host_isotype_name").value,
      part_number: document.getElementById("part_number").value,
      clone_name: document.getElementById("clone_name").value,
      product_category: document.getElementById("product_category").value,
      top_products: document.getElementById("top_products").value,
    };

    let url = "/api/products";
    let method = "POST";

    // if editing, switch to PUT
    if (window.editingProductId) {
      url = `/api/products/${window.editingProductId}`;
      method = "PUT";
    }

    let response = await fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(product),
    });

    console.log("status:", response.status);

    window.editingProductId = null;
    document.getElementById("productForm").reset();
    document.getElementById("formTitle").innerText = "Add New Product";

    loadProducts();
  });
}

const lotForm = document.getElementById("lotForm");

if (lotForm) {
  lotForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    let lot = {
      //product_name: document.getElementById("product_name:").value,
      product_id: Number(document.getElementById("product_id").value),
      lot_number: document.getElementById("lot_number").value,
      creation_date: document.getElementById("creation_date").value,
      expiration_date: document.getElementById("expiration_date").value,
      product_state: document.getElementById("product_state").value,
      test_5uL_concentration_ug_ml: document.getElementById(
        "test_5uL_concentration_ug_ml",
      ).value,
      initial_volume_mL: document.getElementById("initial_volume_ml").value,
      remarks: document.getElementById("remarks").value,
    };

    let url = "/api/lots";
    let method = "POST";

    // EDIT MODE
    if (window.editingLotId) {
      url = `/api/lots/${window.editingLotId}`;
      method = "PUT";
    }

    let response = await fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(lot),
    });

    console.log(await response.text());

    console.log("STATUS:", response.status);

    window.editingLotId = null;
    lotForm.reset();
    document.getElementById("formTitle").innerText = "Add New Lot";

    loadLots();
  });
}

const bulkForm = document.getElementById("bulkForm");

if (bulkForm) {
  bulkForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    let bulk_product = {
      lot_id: Number(document.getElementById("lot_id").value),
      product_id: Number(document.getElementById("product_id").value),
      lot_number: document.getElementById("lot_number").value,
      storage_concentration_ug_mL: Number(
        document.getElementById("storage_concentration_ug_mL").value,
      ),
      current_volume_mL: Number(
        document.getElementById("current_volume_mL").value,
      ),
      location: document.getElementById("location").value,
      buffer: document.getElementById("buffer").value,
      remarks: document.getElementById("remarks").value,
    };

    let url = "/api/bulk_inventory";
    let method = "POST";

    // SAFE VERSION (prevents crash)
    if (window.editing && window.editing.type === "bulk") {
      url = `/api/bulk_inventory/${window.editing.id}`;
      method = "PUT";
    }

    let response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(bulk_product),
    });

    console.log("STATUS:", response.status);

    window.editing.type = null;
    window.editing.id = null;

    bulkForm.reset();
    document.getElementById("formTitle").innerText = "Add New Bulk Product";

    loadBulkInventory();
  });
}

const packagedForm = document.getElementById("packagedForm");

if (packagedForm) {
  packagedForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    let packaged_product = {
      lot_id: Number(document.getElementById("lot_id").value),
      product_id: Number(document.getElementById("product_id").value),
      product_catalog_number: String(
        document.getElementById("product_catalog_number").value,
      ),
      unit_price: Number(document.getElementById("unit_price").value),
      lot_number: document.getElementById("lot_number").value,
      size: document.getElementById("size").value,
      packaging_date: document.getElementById("packaging_date").value,
      packaging_concentration_ug_mL: Number(
        document.getElementById("packaging_concentration_ug_mL").value,
      ),
      location: document.getElementById("location").value,
      qty_remaining: document.getElementById("qty_remaining").value,
      buffer: document.getElementById("buffer").value,
      cost_of_goods: document.getElementById("cost_of_goods").value,
      remarks: document.getElementById("remarks").value,
    };

    let url = "/api/packaged_inventory";
    let method = "POST";

    // SAFE VERSION (prevents crash)
    if (window.editing && window.editing.type === "packaged") {
      url = `/api/packaged_inventory/${window.editing.id}`;
      method = "PUT";
    }

    let response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(packaged_product),
    });

    console.log("STATUS:", response.status);

    window.editing.type = null;
    window.editing.id = null;

    packagedForm.reset();
    document.getElementById("formTitle").innerText = "Add New Packaged Product";

    loadPackagedInventory();
  });
}

async function loadFluorophores() {
  let response = await fetch("/api/fluorophores");
  let data = await response.json();

  let dropdown = document.getElementById("fluorophore_name");

  // IMPORTANT: reset dropdown AND add N/A option
  dropdown.innerHTML = "";

  let naOption = document.createElement("option");
  naOption.value = "";
  naOption.textContent = "N/A";
  dropdown.appendChild(naOption);

  // then add real values
  data.forEach((f) => {
    let option = document.createElement("option");
    option.value = f.fluorophore_name;
    option.textContent = f.fluorophore_name;
    dropdown.appendChild(option);
  });
}

async function loadProductDropdown() {
  let response = await fetch("/api/products");
  let products = await response.json();

  let select = document.getElementById("product_id");

  console.log("select element:", select);

  select.innerHTML = `<option value="">Select a product</option>`;

  products.forEach((p) => {
    select.innerHTML += `
      <option value="${p.product_id}">
        ${p.product_name} — ${p.clone_name}
      </option>
    `;
  });
}

async function loadLotsDropdown() {
  let res = await fetch("/api/lots");
  let lots = await res.json();

  let select = document.getElementById("lot_id");
  select.innerHTML = "";

  lots.forEach((lot) => {
    let option = document.createElement("option");

    option.value = lot.lot_id;

    option.textContent = `Lot ${lot.lot_number} — ${lot.product_name || lot.product_id}`;

    select.appendChild(option);
  });
}

async function loadBulkDropdown() {
  let response = await fetch("/api/lots");
  let products = await response.json();

  let select = document.getElementById("lot_id");

  console.log("select element:", select);

  select.innerHTML = `<option value="">Select a product</option>`;

  products.forEach((l) => {
    select.innerHTML += `
      <option value="${l.product_id}">
        ${l.product_name} — ${l.clone_name}
      </option>
    `;
  });
}

document.addEventListener("DOMContentLoaded", () => {
  loadFluorophores();
  loadLots();
  loadProductDropdown();
  loadLotsDropdown();
  loadBulkDropdown();
});

async function deleteProduct(product_id) {
  if (!confirm("Delete this product?")) return;
  let response = await fetch(`/api/products/${product_id}`, {
    method: "DELETE",
  });

  if (response.ok) {
    console.log("Deleted product:", product_id);
    loadProducts(); // refresh table
  } else {
    console.error("Failed to delete");
  }
}

const productDropdown = document.getElementById("product_id");

if (productDropdown) {
  productDropdown.addEventListener("change", async (e) => {
    let productId = e.target.value;

    let res = await fetch(`/api/lots?product_id=${productId}`);
    let lots = await res.json();

    let lotSelect = document.getElementById("lot_id");
    lotSelect.innerHTML = "";

    lots.forEach((lot) => {
      let opt = document.createElement("option");
      opt.value = lot.lot_id;
      opt.textContent = `Lot ${lot.lot_number}`;
      lotSelect.appendChild(opt);
    });
  });
}

window.updateProduct = async function (product_id) {
  console.log("editing:", product_id);

  let response = await fetch(`/api/products/${product_id}`);
  let product = await response.json();

  document.getElementById("product_name").value = product.product_name || "";
  document.getElementById("ab_name").value = product.ab_name || "";
  document.getElementById("fluorophore_name").value =
    product.fluorophore_name || "";
  document.getElementById("host_isotype_name").value =
    product.host_isotype_name || "";
  document.getElementById("part_number").value = product.part_number || "";
  document.getElementById("clone_name").value = product.clone_name || "";
  document.getElementById("product_category").value =
    product.product_category || "";
  document.getElementById("top_products").value = product.top_products || "NO";

  // switch to edit mode
  window.editingProductId = product_id;

  // CHANGE HEADER TEXT
  document.getElementById("formTitle").innerText = "Edit Product";
};

window.updateLot = async function (lot_id) {
  let response = await fetch(`/api/lots/${lot_id}`);
  let lot = await response.json();
  document.getElementById("product_name").value = lot.product_name || "";
  document.getElementById("lot_number").value = lot.lot_number || "";
  document.getElementById("creation_date").value = lot.creation_date || "";
  document.getElementById("expiration_date").value = lot.expiration_date || "";
  document.getElementById("product_state").value = lot.product_state || "";
  document.getElementById("test_5uL_concentration_ug_ml").value =
    lot.test_5uL_concentration_ug_ml || "";
  document.getElementById("initial_volume_ml").value =
    lot.initial_volume_ml || "";
  document.getElementById("remarks").value = lot.remarks || "";

  // switch to edit mode
  window.editingLotId = lot_id;

  // CHANGE HEADER TEXT
  document.getElementById("formTitle").innerText = "Edit Lot";
};

window.updateBulkProduct = async function (lot_id) {
  console.log("EDIT CLICKED WITH ID:", lot_id);
  let response = await fetch(`/api/bulk_inventory/${lot_id}`);
  let bulk_product = await response.json();

  // fill form fields
  document.getElementById("product_id").value = bulk_product.product_id || "";
  document.getElementById("lot_number").value = bulk_product.lot_number || "";
  document.getElementById("storage_concentration_ug_mL").value =
    bulk_product.storage_concentration_ug_mL || "";
  document.getElementById("current_volume_mL").value =
    bulk_product.current_volume_mL || "";
  document.getElementById("location").value = bulk_product.location || "";
  document.getElementById("buffer").value = bulk_product.buffer || "";
  document.getElementById("remarks").value = bulk_product.remarks || "";

  // set edit mode ONLY
  window.editing.type = "bulk";
  window.editing.id = lot_id;

  // UI update
  document.getElementById("formTitle").innerText = "Edit Bulk Product";
};

window.updatePackagedProduct = async function (packaged_id) {
  console.log("EDIT CLICKED WITH ID:", packaged_id);
  let response = await fetch(`/api/packaged_inventory/${packaged_id}`);
  let packaged_product = await response.json();

  // fill form fields
  document.getElementById("product_id").value =
    packaged_product.product_id || "";
  document.getElementById("lot_id").value = packaged_product.lot_id || "";
  document.getElementById("unit_price").value =
    packaged_product.unit_price || "";
  document.getElementById("packaging_date").value =
    packaged_product.packaging_date || "";
  document.getElementById("packaging_concentration_ug_mL").value =
    packaged_product.packaging_concentration_ug_mL || "";
  document.getElementById("qty_remaining").value =
    packaged_product.qty_remaining || "";
  document.getElementById("product_catalog_number").value =
    packaged_product.product_catalog_number || "";
  document.getElementById("size").value = packaged_product.size || "";
  document.getElementById("location").value = packaged_product.location || "";
  document.getElementById("buffer").value = packaged_product.buffer || "";
  document.getElementById("cost_of_goods").value =
    packaged_product.cost_of_goods || "";
  document.getElementById("remarks").value = packaged_product.remarks || "";

  // set edit mode ONLY
  window.editing.type = "packaged";
  window.editing.id = packaged_id;

  // UI update
  document.getElementById("formTitle").innerText = "Edit Packaged Product";
};

async function deleteLot(lot_id) {
  if (!confirm("Delete this lot?")) return;
  let response = await fetch(`/api/lots/${lot_id}`, {
    method: "DELETE",
  });

  if (response.ok) {
    console.log("Deleted lot:", lot_id);
    loadLots(); // refresh table
  } else {
    console.error("Failed to delete");
  }
}

async function deleteBulkProduct(lot_id) {
  if (!confirm("Delete this bulk?")) return;
  console.log("Deleting:", lot_id);

  let response = await fetch(`/api/bulk_inventory/${lot_id}`, {
    method: "DELETE",
  });

  console.log(await response.json());
}

async function deletePackagedProduct(packaged_id) {
  if (!confirm("Delete this packaged product?")) return;
  console.log("Deleting:", packaged_id);

  let response = await fetch(`/api/packaged_inventory/${packaged_id}`, {
    method: "DELETE",
  });

  console.log(await response.json());
}

window.cancelEdit = function (type) {
  if (type === "product") {
    window.editingProductId = null;
    document.getElementById("productForm").reset();
    document.getElementById("formTitle").innerText = "Add New Product";
  }

  if (type === "lot") {
    window.editingLotId = null;
    document.getElementById("lotForm").reset();
    document.getElementById("formTitle").innerText = "Add New Lot";
  }
  if (type === "bulk_product") {
    window.editingLotId = null;
    document.getElementById("bulkProductForm").reset();
    document.getElementById("formTitle").innerText = "Add New Bulk";
  }
  if (type === "packaged_product") {
    window.editingLotId = null;
    document.getElementById("packagedProductForm").reset();
    document.getElementById("formTitle").innerText = "Add New Packaged Product";
  }
};
