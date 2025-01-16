<?php
include 'db.php';

// Read JSON input
$data = json_decode(file_get_contents('php://input'), true);

// Validate input
if (empty($data['event_id']) || empty($data['seat_number']) || empty($data['captcha'])) {
    echo json_encode(['status' => 'error', 'message' => 'Missing required information']);
    exit;
}

// Validate captcha
session_start();
if ($data['captcha'] !== $_SESSION['captcha']) {
    echo json_encode(['status' => 'error', 'message' => 'Invalid captcha']);
    exit;
}

// Reserve seat in the database
$stmt = $pdo->prepare("UPDATE seats SET status = 'reserved', user_id = ? WHERE event_id = ? AND seat_number = ? AND status = 'available'");
$stmt->execute([$_SESSION['user_id'], $data['event_id'], $data['seat_number']]);

// Return the result
if ($stmt->rowCount() > 0) {
    echo json_encode(['status' => 'success', 'message' => 'Ticket successfully purchased']);
} else {
    echo json_encode(['status' => 'error', 'message' => 'Seat already reserved']);
}
?>
