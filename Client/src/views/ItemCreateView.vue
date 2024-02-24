<template>
  <v-container>
    <v-row class="mb-5">
      <v-col cols="12">
        <v-text-field v-model="search" label="Search Items and Categories" outlined clearable></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>
            Items
            <v-spacer></v-spacer>
            <v-btn color="primary" dark @click="showItemDialog = true">Add Item</v-btn>
          </v-card-title>
          <v-card-text>
            <v-data-table :headers="itemHeaders" :items="filteredItems" :search="search">
              <template v-slot:[`item.action`]="{ item }">
                <v-btn text @click="confirmDeleteItem(item)" class="mx-2">
                  <v-icon small color="red">mdi-delete</v-icon>
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>
            Categories
            <v-spacer></v-spacer>
            <v-btn color="primary" dark @click="showCategoryDialog = true">Add Category</v-btn>
          </v-card-title>
          <v-card-text>
            <v-data-table :headers="categoryHeaders" :items="filteredCategories" :search="search" class="elevation-1">
              <template v-slot:[`item.action`]="{ item }">
                <v-btn text @click="confirmDeleteCategory(item)" class="mx-2">
                  <v-icon small color="red">mdi-delete</v-icon>
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="showItemDialog" max-width="600px">
      <v-card>
        <v-card-title>Add New Item</v-card-title>
        <v-card-text>
          <v-text-field v-model="newItem.name" label="Item Name" outlined></v-text-field>
          <v-text-field v-model="newItem.category" label="Item Category" outlined></v-text-field>
          <v-textarea v-model="newItem.description" label="Item Description" outlined></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="showItemDialog = false">Cancel</v-btn>
          <v-btn color="blue darken-1" text @click="addItem()">Add</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showCategoryDialog" max-width="600px">
      <v-card>
        <v-card-title>Add New Category</v-card-title>
        <v-card-text>
          <v-text-field v-model="newCategory.name" label="Category Name" outlined></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="showCategoryDialog = false">Cancel</v-btn>
          <v-btn color="blue darken-1" text @click="addCategory()">Add</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showDeleteDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">Are you sure?</v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="cancelDelete()">Cancel</v-btn>
          <v-btn color="red darken-1" text @click="confirmDelete()">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios';
export default {
  data: () => ({
    search: '',
    items: [],
    categories: [],
    showItemDialog: false,
    showCategoryDialog: false,
    showDeleteDialog: false,
    deleteType: null,
    deleteItemIndex: null,
    newItem: {
      name: '',
      category: '',
      description: '',
    },
    newCategory: {
      name: '',
    },
    itemHeaders: [
      { title: 'Item Name', key: 'name' },
      { title: 'Item Category', key: 'category', sortable: false },
      { title: 'Item Description', key: 'description', sortable: false },
      { title: 'Actions', key: 'action', sortable: false },
    ],
    categoryHeaders: [
      { title: 'Category Name', key: 'name' },
      { title: 'Actions', key: 'action', sortable: false },
    ],
  }),
  computed: {
    filteredItems() {
      return this.search ? this.items.filter(i => Object.values(i).some(v => v.toLowerCase().includes(this.search.toLowerCase()))) : this.items;
    },
    filteredCategories() {
      return this.search ? this.categories.filter(c => c.name.toLowerCase().includes(this.search.toLowerCase())) : this.categories;
    },
  },
  created() {
    let data = JSON.stringify({
      "ItemName": "Ibprofin",
      "ItemDescription": "Test Description",
      "CategoryName": "TestCategory"
    });

    let config = {
      method: 'get',
      maxBodyLength: Infinity,
      url: 'http://127.0.0.1:5000/item/GetCategories',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiUm9sZUlEIjoxLCJEYXRlQ3JlYXRlZCI6IjIwMjQtMDItMjNUMTU6NTE6MTcuOTY2MzA5In0.eJ8KJO5Dr-b0-Hf7f7ImmBtwhZD-sVIrmt8Xu-UAyKY'
      },
      data: data
    };

    axios.request(config)
      .then((response) => {
        for (var i = 0; i < response.data.length; i++) {
          this.categories.push({ name: response.data[i].CategoryName });
        }
      })
      .catch((error) => {
        console.log(error);
      });

    let data2 = JSON.stringify({
      "ItemName": "Ibprofin",
      "ItemDescription": "Test Description",
      "CategoryName": "TestCategory"
    });

    let config2 = {
      method: 'get',
      maxBodyLength: Infinity,
      url: 'http://127.0.0.1:5000/item/GetAllItems',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiUm9sZUlEIjoxLCJEYXRlQ3JlYXRlZCI6IjIwMjQtMDItMjNUMTU6NTE6MTcuOTY2MzA5In0.eJ8KJO5Dr-b0-Hf7f7ImmBtwhZD-sVIrmt8Xu-UAyKY'
      },
      data: data2
    };

    axios.request(config2)
      .then((response) => {
        this.items = response.data;
      })
      .catch((error) => {
        console.log(error);
      });


  },
  methods: {
    addItem() {
      this.items.push({ ...this.newItem });
      this.newItem = { name: '', category: '', description: '' };
      this.showItemDialog = false;
    },
    addCategory() {
      this.categories.push({ ...this.newCategory });
      this.newCategory = { name: '' };
      this.showCategoryDialog = false;
    },
    confirmDeleteItem(item) {
      this.deleteType = 'item';
      this.deleteItemIndex = this.items.indexOf(item);
      this.showDeleteDialog = true;
    },
    confirmDeleteCategory(category) {
      this.deleteType = 'category';
      this.deleteItemIndex = this.categories.indexOf(category);
      this.showDeleteDialog = true;
    },
    cancelDelete() {
      this.showDeleteDialog = false;
      this.deleteType = null;
      this.deleteItemIndex = null;
    },
    confirmDelete() {
      if (this.deleteType === 'item') {
        this.items.splice(this.deleteItemIndex, 1);
      } else if (this.deleteType === 'category') {
        this.categories.splice(this.deleteItemIndex, 1);
      }
      this.cancelDelete();
    },
  },
};
</script>

<style scoped></style>
