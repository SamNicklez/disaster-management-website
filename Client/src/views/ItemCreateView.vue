<template>
  <v-dialog v-model="showDeleteDialog" persistent max-width="300px">
    <v-card>
      <v-card-title class="text-h5">Confirm Delete</v-card-title>
      <v-card-text>Are you sure you want to delete this {{ deleteType }}?</v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="showDeleteDialog = false">Cancel</v-btn>
        <v-btn color="red darken-1" text @click="confirmDelete()">Delete</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <v-card style="margin: auto; max-width: 70vw">
    <v-tabs v-model="tab" color="orange">
      <v-tab value="one">Item Details</v-tab>
      <v-tab value="two">Category Details</v-tab>
    </v-tabs>
    <v-card-text>
      <v-window v-model="tab">
        <v-window-item value="one">
          <v-container>
            <v-row class="mb-5">
              <v-col cols="12">
                <v-text-field
                  v-model="search"
                  label="Search Items"
                  outlined
                  clearable
                ></v-text-field>
              </v-col>
            </v-row>

            <v-card>
              <v-card-title>
                Items
                <v-spacer></v-spacer>
                <v-btn color="primary" id="additem" dark @click="showItemDialog = true"
                  >Add Item</v-btn
                >
              </v-card-title>
              <v-card-text>
                <v-data-table :headers="itemHeaders" :items="filteredItems" :search="search">
                  <template v-slot:[`item.action`]="{ item }">
                    <v-btn text @click="confirmDeleteItem(item)" class="mx-2">
                      <v-icon small color="red">mdi-delete</v-icon>
                    </v-btn>
                  </template>
                  <template v-slot:[`item.edit`]="{ item }">
                    <v-btn text @click="editItem(item)" class="mx-2">
                      <v-icon small color="blue">mdi-pencil</v-icon>
                    </v-btn>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
            <v-dialog v-model="showItemDialog" max-width="600px">
              <v-card>
                <v-card-title>Add New Item</v-card-title>
                <v-card-text>
                  <v-text-field v-model="newItem.name" label="Item Name" outlined></v-text-field>
                  <v-autocomplete
                    v-model="newItem.category"
                    label="Item Category"
                    outlined
                    :items="categoryArray"
                  ></v-autocomplete>
                  <v-textarea
                    v-model="newItem.description"
                    label="Item Description"
                    outlined
                  ></v-textarea>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="showItemDialog = false">Cancel</v-btn>
                  <v-btn color="blue darken-1" text @click="addItem()">Add</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-container>
        </v-window-item>

        <v-window-item value="two">
          <v-container>
            <v-row class="mb-5">
              <v-col cols="12">
                <v-text-field
                  v-model="search"
                  label="Search Categories"
                  outlined
                  clearable
                ></v-text-field>
              </v-col>
            </v-row>
            <v-card>
              <v-card-title>
                Categories
                <v-spacer></v-spacer>
                <v-btn color="primary" dark @click="showCategoryDialog = true" id="addcategory"
                  >Add Category</v-btn
                >
              </v-card-title>
              <v-card-text>
                <v-data-table
                  :headers="categoryHeaders"
                  :items="filteredCategories"
                  :search="search"
                >
                  <template v-slot:[`item.action`]="{ item }">
                    <v-btn text @click="confirmDeleteCategory(item)" class="mx-2">
                      <v-icon small color="red">mdi-delete</v-icon>
                    </v-btn>
                  </template>
                  <template v-slot:[`item.edit`]="{ item }">
                    <v-btn text @click="editCategory(item)" class="mx-2">
                      <v-icon small color="blue">mdi-pencil</v-icon>
                    </v-btn>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
            <v-dialog v-model="showCategoryDialog" max-width="600px">
              <v-card>
                <v-card-title>Add New Category</v-card-title>
                <v-card-text>
                  <v-text-field
                    v-model="newCategory.name"
                    label="Category Name"
                    outlined
                  ></v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="showCategoryDialog = false"
                    >Cancel</v-btn
                  >
                  <v-btn color="blue darken-1" text @click="addCategory()">Add</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-container>
        </v-window-item>
      </v-window>
    </v-card-text>
  </v-card>
</template>

<script>
import axios from 'axios'
import { user } from '../stores/user.js'
import { alertStore } from '../stores/alert.js'
export default {
  data: () => ({
    search: '',
    items: [],
    categories: [],
    editIndex: -1,
    editCategoryIndex: -1,
    categoryArray: [],
    showItemDialog: false,
    showCategoryDialog: false,
    showDeleteDialog: false,
    deleteType: null,
    deleteItemIndex: null,
    tab: null,
    newItem: {
      name: '',
      category: '',
      description: ''
    },
    newCategory: {
      name: ''
    },
    itemHeaders: [
      { title: 'Item Name', key: 'name' },
      { title: 'Item Category', key: 'category', sortable: false },
      { title: 'Item Description', key: 'description', sortable: false },
      { title: 'Actions', key: 'action', sortable: false },
      { title: 'Edit', key: 'edit', sortable: false } // New edit column
    ],
    categoryHeaders: [
      { title: 'Category Name', key: 'name' },
      { title: 'Actions', key: 'action', sortable: false },
      { title: 'Edit', key: 'edit', sortable: false } // New edit column
    ]
  }),
  computed: {
    filteredItems() {
      return this.search
        ? this.items.filter((i) =>
            Object.values(i).some((v) => v.toLowerCase().includes(this.search.toLowerCase()))
          )
        : this.items
    },
    filteredCategories() {
      return this.search
        ? this.categories.filter((c) => c.name.toLowerCase().includes(this.search.toLowerCase()))
        : this.categories
    }
  },
  created() {
    let userData = user()
    let data = ''
    let config = {
      method: 'get',
      maxBodyLength: Infinity,
      url: 'http://127.0.0.1:5000/item/GetCategories',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + userData.getToken
      },
      data: data
    }

    axios
      .request(config)
      .then((response) => {
        for (var i = 0; i < response.data.length; i++) {
          this.categories.push({ name: response.data[i].CategoryName })
          this.categoryArray.push(response.data[i].CategoryName)
        }
      })
      .catch((error) => {
        alertStore.showError(error.response.data.error)
      })

    let data2 = ''

    let config2 = {
      method: 'get',
      maxBodyLength: Infinity,
      url: 'http://127.0.0.1:5000/item/GetAllItems',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + userData.getToken
      },
      data: data2
    }

    axios
      .request(config2)
      .then((response) => {
        this.items = response.data
      })
      .catch((error) => {
        alertStore.showError(error.response.data.error)
      })
  },
  methods: {
    confirmDeleteItem(item) {
      this.deleteType = 'item'
      this.deleteItemIndex = this.items.indexOf(item)
      this.showDeleteDialog = true
    },
    confirmDeleteCategory(category) {
      this.deleteType = 'category'
      this.deleteItemIndex = this.categories.indexOf(category)
      this.showDeleteDialog = true
    },
    cancelDelete() {
      this.showDeleteDialog = false
      this.deleteType = null
      this.deleteItemIndex = null
    },
    confirmDelete() {
      let userData = user()
      if (this.deleteType === 'item') {
        let data = JSON.stringify({
          ItemName: this.items[this.deleteItemIndex].name
        })

        let config = {
          method: 'post',
          maxBodyLength: Infinity,
          url: 'http://127.0.0.1:5000/item/DeleteItem',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + userData.getToken
          },
          data: data
        }

        axios
          .request(config)
          .then(() => {
            this.items.splice(this.deleteItemIndex, 1)
          })
          .catch((error) => {
            alertStore.showError(error.response.data.error)
          })
      } else if (this.deleteType === 'category') {
        let userData = user()
        let data = JSON.stringify({
          CategoryName: this.categories[this.deleteItemIndex].name
        })

        let config = {
          method: 'post',
          maxBodyLength: Infinity,
          url: 'http://127.0.0.1:5000/item/DeleteCategory',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + userData.getToken
          },
          data: data
        }

        axios
          .request(config)
          .then(() => {
            this.categories.splice(this.deleteItemIndex, 1)
          })
          .catch((error) => {
            alertStore.showError(error.response.data.error)
          })
      }
      this.cancelDelete()
    },
    editItem(item) {
      this.newItem = { ...item }
      this.showItemDialog = true
      this.editIndex = this.items.findIndex((i) => i.name === item.name)
    },

    editCategory(category) {
      this.newCategory = { ...category }
      this.showCategoryDialog = true
    },
    addItem() {
      let userData = user()
      if (this.editIndex === -1) {
        let data = JSON.stringify({
          ItemName: this.newItem.name,
          CategoryName: this.newItem.category,
          ItemDescription: this.newItem.description
        })

        let config = {
          method: 'post',
          maxBodyLength: Infinity,
          url: 'http://127.0.0.1:5000/item/CreateItem',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + userData.getToken
          },
          data: data
        }

        axios
          .request(config)
          .then(() => {
            this.items.push({ ...this.newItem })
          })
          .catch((error) => {
            alertStore.showError(error.response.data.error)
          })
      } else {
        let data = JSON.stringify({
          ItemName: this.items[this.editIndex].name,
          CategoryName: this.newItem.category,
          NewName: this.newItem.name,
          NewDescription: this.newItem.description
        })

        let config = {
          method: 'post',
          maxBodyLength: Infinity,
          url: 'http://127.0.0.1:5000/item/EditItem',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + userData.getToken
          },
          data: data
        }

        axios
          .request(config)
          .then(() => {
            this.items[this.editIndex] = { ...this.newItem }
          })
          .catch((error) => {
            alertStore.showError(error.response.data.error)
          })
      }
      this.newItem = { name: '', category: '', description: '' }
      this.showItemDialog = false
      this.editIndex = -1
    },

    addCategory() {
      let userData = user()
      if (this.editCategoryIndex === -1) {
        // Adding a new category
        let name = this.newCategory.name
        let data = JSON.stringify({
          CategoryName: this.newCategory.name
        })

        let config = {
          method: 'post',
          maxBodyLength: Infinity,
          url: 'http://127.0.0.1:5000/item/CreateCategory',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + userData.getToken
          },
          data: data
        }

        axios
          .request(config)
          .then(() => {
            this.categories.push({ name: name })
          })
          .catch((error) => {
            alertStore.showError(error.response.data.error)
          })
      } else {
        // Editing an existing category
        let data = JSON.stringify({
          NewCategoryName: this.newCategory.name,
          CategoryName: this.categories[this.editCategoryIndex].name
        })

        let config = {
          method: 'post',
          maxBodyLength: Infinity,
          url: 'http://127.0.0.1:5000/item/EditCategory',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + userData.getToken
          },
          data: data
        }

        axios
          .request(config)
          .then(() => {
            this.categories[this.editCategoryIndex] = { ...this.newCategory }
          })
          .catch((error) => {
            alertStore.showError(error.response.data.error)
          })
      }
      // Reset
      this.newCategory = { name: '' }
      this.showCategoryDialog = false
      this.editCategoryIndex = -1 // Reset edit index for categories
    }
  }
}
</script>

<style scoped></style>
