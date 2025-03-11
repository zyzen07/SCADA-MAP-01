CREATE DATABASE ip_topology;

USE ip_topology;

CREATE TABLE devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_name VARCHAR(50),
    image_path VARCHAR(200),
    ip_address VARCHAR(50),
    mac_address VARCHAR(50),
    interface VARCHAR(50),
    os VARCHAR(50),
    status VARCHAR(20),
    protocol VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
