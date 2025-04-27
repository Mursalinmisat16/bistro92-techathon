import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ServerIP from '../ServerIP.jsx'

function OrdersPage() {
  const [pendingOrders, setPendingOrders] = useState([]);
  const [servedOrders, setServedOrders] = useState([]);

  const fetchOrders = async () => {
    try {
      const response = await axios.get(`${ServerIP()}/orders/`);
      const allOrders = response.data;

      const pending = allOrders.filter(order => order.status === 'pending');
      const served = allOrders.filter(order => order.status === 'served');

      setPendingOrders(pending);
      setServedOrders(served);
      console.log(response)
    } catch (error) {
      console.error('Failed to fetch orders', error);
    }
  };

  const serveOrder = async (orderId) => {
    try {
      await axios.patch(`http://127.0.0.1:8000/order/${orderId}/serve`);
      fetchOrders();
    } catch (error) {
      console.error('Failed to serve order', error);
    }
  };

  const deleteOrder = async (orderId) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/order/${orderId}`);
      fetchOrders();
    } catch (error) {
      console.error('Failed to delete order', error);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const renderTable = (orders, isPending) => (
    <div className="overflow-x-auto mb-10">
      <table className="min-w-full bg-white rounded-lg shadow-md">
        <thead className="bg-indigo-600 text-white">
          <tr>
            <th className="py-3 px-4">#</th>
            <th className="py-3 px-4">Table No</th>
            <th className="py-3 px-4">Order Items</th>
            <th className="py-3 px-4">Time</th>
            <th className="py-3 px-4">Status</th>
            <th className="py-3 px-4">Action</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((order, index) => (
            <tr key={order.order_id} className="border-t">
              <td className="py-3 px-4 text-center">{index + 1}</td>
              <td className="py-3 px-4 text-center">{order.table_number}</td>
              <td className="py-3 px-4">
                {order.items.map((item, idx) => (
                  <div key={idx} className="flex justify-between">
                    <span>{item.item_name}</span>
                    <span>x{item.quantity}</span>
                  </div>
                ))}
              </td>
              <td className="py-3 px-4 text-center">
                {(new Date(order.created_at).toLocaleString())}
              </td>
              <td className="py-3 px-4 text-center capitalize">{order.status}</td>
              <td className="py-3 px-4 text-center">
                {isPending ? (
                  <button
                    onClick={() => serveOrder(order.order_id)}
                    className="bg-green-500 hover:bg-green-600 text-white font-semibold py-1 px-4 rounded"
                  >
                    Serve
                  </button>
                ) : (
                  <button
                    onClick={() => deleteOrder(order.order_id)}
                    className="bg-red-500 hover:bg-red-600 text-white font-semibold py-1 px-4 rounded"
                  >
                    Delete
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-5xl font-bold text-center mb-12 text-indigo-700">BISTRO 92</h1>

      <h2 className="text-2xl font-semibold text-gray-700 mb-4">Pending Orders</h2>
      {renderTable(pendingOrders, true)}

      <h2 className="text-2xl font-semibold text-gray-700 mb-4">Served Orders</h2>
      {renderTable(servedOrders, false)}
    </div>
  );
}

export default OrdersPage;
