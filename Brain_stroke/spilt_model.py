import os
import shutil
import random

# ====== BASE DIRECTORY ======
base_dir = os.path.dirname(os.path.abspath(__file__))

# ====== USE TRAIN DATA (IMPORTANT) ======
source_dir = os.path.join(base_dir, "archive", "Brain_Stroke_CT-SCAN_image", "Train")
output_dir = os.path.join(base_dir, "brain_split")

# ====== CLASSES ======
classes = ["Normal", "Stroke"]

# ====== SPLIT RATIOS ======
train_ratio = 0.7
val_ratio = 0.15
test_ratio = 0.15

print("📂 Source Directory:", source_dir)

for cls in classes:
    cls_path = os.path.join(source_dir, cls)

    if not os.path.exists(cls_path):
        print(f"❌ Folder not found: {cls_path}")
        continue

    images = os.listdir(cls_path)

    random.shuffle(images)

    total = len(images)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)

    train_imgs = images[:train_end]
    val_imgs = images[train_end:val_end]
    test_imgs = images[val_end:]

    print(f"{cls} → Train:{len(train_imgs)}, Val:{len(val_imgs)}, Test:{len(test_imgs)}")

    for split, img_list in zip(
        ["train", "val", "test"],
        [train_imgs, val_imgs, test_imgs]
    ):
        split_folder = os.path.join(output_dir, split, cls)
        os.makedirs(split_folder, exist_ok=True)

        for img in img_list:
            src = os.path.join(cls_path, img)
            dst = os.path.join(split_folder, img)

            if os.path.exists(src):
                shutil.copy(src, dst)

print("✅ Dataset split completed successfully!")