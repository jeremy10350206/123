<?php
include 'db.php';

// Read JSON input
$data = json_decode(file_get_contents('php://input'), true);

// Validate input
if (empty($data['username']) || empty($data['password']) || empty($data['email'])) {
    echo json_encode(['status' => 'error', 'message' => 'Please fill in all fields']);
    exit;
}

// Hash the password
$password_hash = password_hash($data['password'], PASSWORD_BCRYPT);

// Insert user into the database
$stmt = $pdo->prepare("INSERT INTO users (username, password, email) VALUES (?, ?, ?)");
try {
    $stmt->execute([$data['username'], $password_hash, $data['email']]);
    echo json_encode(['status' => 'success', 'message' => 'Registration successful']);
} catch (PDOException $e) {
    echo json_encode(['status' => 'error', 'message' => 'Username or email already exists']);
}
?>
