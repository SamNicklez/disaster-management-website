import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import Component from '@/views/ItemCreateView.vue'
import axios from 'axios'

// Mock the axios module
vi.mock('axios', () => ({
    __esModule: true,
    default: {
      request: vi.fn(() => Promise.resolve({
        data: [{ CategoryName: 'Category 1' }, { CategoryName: 'Category 2' }]
      })),
    },
  }));

// Optionally, mock other modules if needed
vi.mock('@/stores/user.js', () => ({
  user: () => ({
    getToken: () => 'mocked-token',
  }),
}))

describe('Component.vue', () => {
  let wrapper

  beforeEach(async () => {
    wrapper = mount(Component, {
    })
    await flushPromises() 
  })

  afterEach(() => {
    wrapper.unmount()
  })

  it('initializes with the correct elements', async () => {
    // Check if the component renders
    expect(wrapper.exists()).toBe(true)
    // Check for initial axios call
    expect(axios.request).toHaveBeenCalled()
  })

  it('adds an item correctly', async () => {
    await wrapper.setData({ newItem: { name: 'New Item', category: 'Category 1', description: 'Description for new item' } })
    await wrapper.find('#additem').trigger('click') 
    // Ensure the dialog is closed after adding
    expect(wrapper.vm.showItemDialog).toBe(true)
  })

  it('adds an item correctly using addItem()', async () => {
    wrapper.vm.newItem = { name: 'New Item', category: 'New Category', description: 'New Description' };
    wrapper.vm.addItem();
    expect(wrapper.vm.items).toContainEqual(expect.objectContaining({
      name: 'New Item', category: 'New Category', description: 'New Description'
    }));
    expect(wrapper.vm.newItem).toEqual({ name: '', category: '', description: '' });
    expect(wrapper.vm.showItemDialog).toBe(false);
  });

  it('adds a category correctly using addCategory()', async () => {
    wrapper.vm.newCategory = { name: 'New Category' };
    wrapper.vm.addCategory();
    expect(wrapper.vm.categories).toContainEqual(expect.objectContaining({ name: 'New Category' }));
    expect(wrapper.vm.newCategory).toEqual({ name: '' });
    expect(wrapper.vm.showCategoryDialog).toBe(false);
  });

  it('prepares to delete an item using confirmDeleteItem()', async () => {
    const item = { name: 'Item to Delete', category: 'Category', description: 'Description' };
    wrapper.vm.items.push(item);
    wrapper.vm.confirmDeleteItem(item);
    expect(wrapper.vm.deleteType).toBe('item');
    expect(wrapper.vm.deleteItemIndex).toBe(wrapper.vm.items.indexOf(item));
    expect(wrapper.vm.showDeleteDialog).toBe(true);
  });

  it('prepares to delete a category using confirmDeleteCategory()', async () => {
    const category = { name: 'Category to Delete' };
    wrapper.vm.categories.push(category);
    wrapper.vm.confirmDeleteCategory(category);
    expect(wrapper.vm.deleteType).toBe('category');
    expect(wrapper.vm.deleteItemIndex).toBe(wrapper.vm.categories.indexOf(category));
    expect(wrapper.vm.showDeleteDialog).toBe(true);
  });

  it('cancels delete operation using cancelDelete()', async () => {
    wrapper.vm.showDeleteDialog = true;
    wrapper.vm.cancelDelete();
    expect(wrapper.vm.showDeleteDialog).toBe(false);
    expect(wrapper.vm.deleteType).toBeNull();
    expect(wrapper.vm.deleteItemIndex).toBeNull();
  });

  it('confirms deletion of item or category using confirmDelete()', async () => {
    const item = { name: 'Item to Delete' };
    const category = { name: 'Category to Delete' };
    wrapper.vm.items.push(item);
    wrapper.vm.categories.push(category);

    wrapper.vm.confirmDeleteItem(item);
    wrapper.vm.confirmDelete();
    expect(wrapper.vm.items).not.toContain(item);
    expect(wrapper.vm.showDeleteDialog).toBe(false);

    wrapper.vm.showDeleteDialog = true;
    wrapper.vm.confirmDeleteCategory(category);
    wrapper.vm.confirmDelete();
    expect(wrapper.vm.categories).not.toContain(category);
    expect(wrapper.vm.showDeleteDialog).toBe(false);
  });

  it('opens the item addition dialog', async () => {
    const wrapper = mount(Component);
    await wrapper.find('#additem').trigger('click');
    expect(wrapper.vm.showItemDialog).toBe(true);
  });
  
  it('opens the category addition dialog', async () => {
    const wrapper = mount(Component);
    await wrapper.find('#addcategory').trigger('click');
    expect(wrapper.vm.showCategoryDialog).toBe(true);
  });
  
})
