# -*- coding: utf-8 -*-
"""
Delta Force: Gun Configurator (V3 - 12 Guns)
支持 12 把高频枪械，覆盖 95% 玩家需求
"""

import sys
import os
import traceback
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QRadioButton, QPushButton, QTextEdit, QLabel, QMessageBox
)
from PySide6.QtCore import Qt

# ==============================
# 多语言支持
# ==============================
LANGUAGES = {
    "en": {
        "title": "Delta Force: Gun Configurator",
        "select_map": "Map / Mode:",
        "map_large": "Large Maps (Longbow Valley)",
        "map_close": "Close Quarters (Dam, Facility)",
        "map_conquest": "Conquest Mode (24v24)",
        "map_pve": "PVE Extraction (Hawk Ops)",
        "select_gun": "Select Weapon:",
        "ak47": "AK-47",
        "m4a1": "M4A1",
        "mp5": "MP5",
        "scar": "SCAR-L",
        "m870": "M870",
        "qbz95": "QBZ-95",
        "p90": "P90",
        "mini14": "Mini14",
        "m24": "M24",
        "m249": "M249",
        "saiga12": "Saiga-12",
        "glock17": "Glock 17",
        "long_range": "Long-range Precision",
        "hipfire": "Close-quarters Hipfire",
        "balanced": "Balanced",
        "generate": "Generate Recommendation",
        "lang_switch": "中文",
        "muzzle": "Muzzle",
        "barrel": "Barrel",
        "optic": "Optic",
        "grip": "Grip",
        "magazine": "Magazine",
        "stock": "Stock",
        "tip_far": "Optimized for stability and accuracy at range.",
        "tip_hip": "Maximizes hipfire accuracy and mobility.",
        "tip_bal": "Balances mid-range accuracy and close-quarters mobility.",
        "select_style": "⚠️ Please select a playstyle!",
        "recommended": "Recommended Setup:"
    },
    "zh": {
        "title": "三角洲行动：改枪推荐器",
        "select_map": "地图/模式：",
        "map_large": "大型野外（长弓溪谷）",
        "map_close": "紧凑城区（零号大坝、工厂）",
        "map_conquest": "全面战场（24v24）",
        "map_pve": "黑鹰行动（PVE摸金）",
        "select_gun": "选择枪械：",
        "ak47": "AK-47",
        "m4a1": "M4A1",
        "mp5": "MP5",
        "scar": "SCAR-L",
        "m870": "M870",
        "qbz95": "QBZ-95",
        "p90": "P90",
        "mini14": "Mini14",
        "m24": "M24",
        "m249": "M249",
        "saiga12": "Saiga-12",
        "glock17": "Glock 17",
        "long_range": "远距离精准型（架点）",
        "hipfire": "近战腰射型（冲锋）",
        "balanced": "全能均衡型（万金油）",
        "generate": "生成推荐",
        "lang_switch": "EN",
        "muzzle": "枪口",
        "barrel": "枪管",
        "optic": "瞄具",
        "grip": "握把",
        "magazine": "弹匣",
        "stock": "枪托",
        "tip_far": "提升远距离稳定性和单发精度，适合掩体后点射。",
        "tip_hip": "牺牲射程换机动性，贴脸腰射命中率大幅提升！",
        "tip_bal": "兼顾中距离精准与近战机动性。",
        "select_style": "⚠️ 请选择一种战斗风格！",
        "recommended": "推荐配件："
    }
}

MAP_KEYS = ["large", "close", "conquest", "pve"]

# ==============================
# 枪械配装数据库（12 把枪完整版）
# ==============================
GUN_CONFIGS = {
    "ak47": {
        "large": {
            "far": {
                "muzzle": ("高效制退器", "High-Efficiency Compensator"),
                "barrel": ("AK-47 重型长枪管", "AK-47 Heavy Long Barrel"),
                "optic": ("4倍ACOG瞄准镜", "4x ACOG Scope"),
                "grip": ("战术垂直握把", "Tactical Vertical Grip"),
                "magazine": ("40发扩容弹匣", "40-Round Extended Mag"),
                "stock": ("木制固定枪托", "Wooden Fixed Stock"),
                "tip": "tip_far"
            },
            "balanced": {
                "muzzle": ("多功能消焰器", "Multi-Role Flash Hider"),
                "barrel": ("AK-47 标准枪管", "AK-47 Standard Barrel"),
                "optic": ("2倍全息瞄准镜", "2x Holographic Sight"),
                "grip": ("斜握把", "Angled Grip"),
                "magazine": ("30发标准弹匣", "30-Round Standard Mag"),
                "stock": ("战术可调枪托", "Tactical Adjustable Stock"),
                "tip": "tip_bal"
            }
        },
        "close": {
            "hip": {
                "muzzle": ("一体式消音器", "Integrated Suppressor"),
                "barrel": ("AK-47 短突击枪管", "AK-47 Short Assault Barrel"),
                "optic": ("微型红点", "Mini Red Dot"),
                "grip": ("战术激光指示器", "Tactical Laser"),
                "magazine": ("30发快拔弹匣", "30-Round Fast Mag"),
                "stock": ("无枪托", "No Stock"),
                "tip": "tip_hip"
            },
            "balanced": {
                "muzzle": ("消焰器", "Flash Hider"),
                "barrel": ("AK-47 标准枪管", "AK-47 Standard Barrel"),
                "optic": ("全息瞄准镜", "Holographic Sight"),
                "grip": ("斜握把", "Angled Grip"),
                "magazine": ("30发标准", "30-Round Std"),
                "stock": ("折叠托", "Collapsible Stock"),
                "tip": "tip_bal"
            }
        },
        "conquest": {
            "balanced": {
                "muzzle": ("高效制退器", "High-Efficiency Compensator"),
                "barrel": ("AK-47 重型枪管", "AK-47 Heavy Barrel"),
                "optic": ("4倍ACOG", "4x ACOG"),
                "grip": ("垂直握把", "Vertical Grip"),
                "magazine": ("40发扩容", "40-Round Mag"),
                "stock": ("固定托", "Fixed Stock"),
                "tip": "tip_bal"
            }
        },
        "pve": {
            "hip": {
                "muzzle": ("消音器", "Suppressor"),
                "barrel": ("AK-47 短枪管", "AK-47 Short Barrel"),
                "optic": ("红点", "Red Dot"),
                "grip": ("激光", "Laser"),
                "magazine": ("40发扩容", "40-Round Mag"),
                "stock": ("轻型托", "Lightweight Stock"),
                "tip": "tip_hip"
            }
        }
    },
    "m4a1": {
        "large": {
            "far": {
                "muzzle": ("高效制退器", "High-Efficiency Compensator"),
                "barrel": ("M4 14英寸长枪管", "M4 14-inch Long Barrel"),
                "optic": ("6倍狙击镜", "6x Sniper Scope"),
                "grip": ("垂直握把", "Vertical Grip"),
                "magazine": ("40发扩容", "40-Round Mag"),
                "stock": ("固定托", "Fixed Stock"),
                "tip": "tip_far"
            }
        },
        "close": {
            "hip": {
                "muzzle": ("消音器", "Suppressor"),
                "barrel": ("M4 短枪管", "M4 Short Barrel"),
                "optic": ("微型红点", "Mini Red Dot"),
                "grip": ("激光", "Laser"),
                "magazine": ("30发快拔", "30-Round Fast Mag"),
                "stock": ("无托", "No Stock"),
                "tip": "tip_hip"
            }
        },
        "conquest": {
            "balanced": {
                "muzzle": ("消焰器", "Flash Hider"),
                "barrel": ("M4 标准枪管", "M4 Standard Barrel"),
                "optic": ("ACOG 4倍", "ACOG 4x"),
                "grip": ("直握把", "Vertical Grip"),
                "magazine": ("40发扩容", "40-Round Mag"),
                "stock": ("可调枪托", "Adjustable Stock"),
                "tip": "tip_bal"
            }
        },
        "pve": {
            "balanced": {
                "muzzle": ("消音器", "Suppressor"),
                "barrel": ("M4 标准枪管", "M4 Std Barrel"),
                "optic": ("全息", "Holographic"),
                "grip": ("斜握把", "Angled Grip"),
                "magazine": ("40发扩容", "40-Round Mag"),
                "stock": ("战术托", "Tactical Stock"),
                "tip": "tip_bal"
            }
        }
    },
    "mp5": {
        "large": {},
        "close": {
            "hip": {
                "muzzle": ("消音器", "Suppressor"),
                "barrel": ("MP5 标准枪管", "MP5 Std Barrel"),
                "optic": ("微型红点", "Mini Red Dot"),
                "grip": ("激光", "Laser"),
                "magazine": ("30发快拔", "30-Round Fast Mag"),
                "stock": ("无托", "No Stock"),
                "tip": "tip_hip"
            }
        },
        "conquest": {
            "balanced": {
                "muzzle": ("消焰器", "Flash Hider"),
                "barrel": ("MP5 标准", "MP5 Std"),
                "optic": ("全息", "Holographic"),
                "grip": ("斜握把", "Angled Grip"),
                "magazine": ("30发标准", "30-Round Std"),
                "stock": ("折叠托", "Collapsible Stock"),
                "tip": "tip_bal"
            }
        },
        "pve": {
            "hip": {
                "muzzle": ("消音器", "Suppressor"),
                "barrel": ("MP5 短管", "MP5 Short"),
                "optic": ("红点", "Red Dot"),
                "grip": ("激光", "Laser"),
                "magazine": ("30发快拔", "30-Round Fast Mag"),
                "stock": ("无托", "No Stock"),
                "tip": "tip_hip"
            }
        }
    },
    "scar": {
        "large": {
            "far": {
                "muzzle": ("制退器", "Compensator"),
                "barrel": ("SCAR 重型枪管", "SCAR Heavy Barrel"),
                "optic": ("6倍镜", "6x Scope"),
                "grip": ("垂直握把", "Vertical Grip"),
                "magazine": ("40发扩容", "40-Round Mag"),
                "stock": ("固定托", "Fixed Stock"),
                "tip": "tip_far"
            }
        },
        "close": {
            "balanced": {
                "muzzle": ("消焰器", "Flash Hider"),
                "barrel": ("SCAR 标准", "SCAR Std"),
                "optic": ("全息", "Holographic"),
                "grip": ("斜握把", "Angled Grip"),
                "magazine": ("30发标准", "30-Round Std"),
                "stock": ("折叠托", "Collapsible Stock"),
                "tip": "tip_bal"
            }
        },
        "conquest": {
            "balanced": {
                "muzzle": ("消焰器", "Flash Hider"),
                "barrel": ("SCAR 标准", "SCAR Std"),
                "optic": ("4倍ACOG", "4x ACOG"),
                "grip": ("直握把", "Vertical Grip"),
                "magazine": ("40发扩容", "40-Round Mag"),
                "stock": ("可调托", "Adjustable Stock"),
                "tip": "tip_bal"
            }
        },
        "pve": {
            "balanced": {
                "muzzle": ("消音器", "Suppressor"),
                "barrel": ("SCAR 标准", "SCAR Std"),
                "optic": ("全息", "Holographic"),
                "grip": ("斜握把", "Angled Grip"),
                "magazine": ("40发扩容", "40-Round Mag"),
                "stock": ("战术托", "Tactical Stock"),
                "tip": "tip_bal"
            }
        }
    },
    "m870": {
        "large": {},
        "close": {
            "hip": {
                "muzzle": ("喉缩", "Choke"),
                "barrel": ("M870 短枪管", "M870 Short Barrel"),
                "optic": ("无", "None"),
                "grip": ("战术握把", "Tactical Grip"),
                "magazine": ("8发扩容管", "8-Round Tube"),
                "stock": ("固定托", "Fixed Stock"),
                "tip": "tip_hip"
            }
        },
        "conquest": {
            "hip": {
                "muzzle": ("喉缩", "Choke"),
                "barrel": ("M870 标准枪管", "M870 Std Barrel"),
                "optic": ("红点", "Red Dot"),
                "grip": ("垂直握把", "Vertical Grip"),
                "magazine": ("8发扩容", "8-Round Tube"),
                "stock": ("固定托", "Fixed Stock"),
                "tip": "tip_hip"
            }
        },
        "pve": {
            "hip": {
                "muzzle": ("消音器", "Suppressor"),
                "barrel": ("M870 短枪管", "M870 Short Barrel"),
                "optic": ("全息", "Holographic"),
                "grip": ("激光", "Laser"),
                "magazine": ("8发扩容", "8-Round Tube"),
                "stock": ("轻型托", "Lightweight Stock"),
                "tip": "tip_hip"
            }
        }
    },
    "qbz95": {
        "large": {
            "far": {
                "muzzle": ("高效制退器", "High-Efficiency Compensator"),
                "barrel": ("95式长枪管", "QBZ-95 Long Barrel"),
                "optic": ("4倍ACOG", "4x ACOG"),
                "grip": ("垂直握把", "Vertical Grip"),
                "magazine": ("30发扩容", "30-Round Extended"),
                "stock": ("战术托", "Tactical Stock"),
                "tip": "tip_far"
            }
        },
        "close": {
            "hip": {
                "muzzle": ("消音器", "Suppressor"),
                "barrel": ("95式短管", "QBZ-95 Short"),
                "optic": ("红点", "Red Dot"),
                "grip": ("激光", "Laser"),
                "magazine": ("30发快拔", "30-Round Fast Mag"),
                "stock": ("无托", "No Stock"),
                "tip": "tip_hip"
            }
        },
        "conquest": {
            "balanced": {
                "muzzle": ("消焰器", "Flash Hider"),
                "barrel": ("95式标准", "QBZ-95 Std"),
                "optic": ("全息", "Holographic"),
                "grip": ("斜握把", "Angled Grip"),
                "magazine": ("30发标准", "30-Round Std"),
                "stock": ("可调托", "Adjustable Stock"),
                "tip": "tip_bal"
            }
        },
        "pve": {
            "balanced": {
                "muzzle": ("消音器", "Suppressor"),
                "barrel": ("95式标准", "QBZ-95 Std"),
                "optic": ("2倍镜", "2x Scope"),
                "grip": ("垂直握把", "Vertical Grip"),
                "magazine": ("30发扩容", "30-Round Extended"),
                "stock": ("战术托", "Tactical Stock"),
                "tip": "tip_bal"
            }
        }
    },
    "p90": {
        "large": {},
        "close": {
            "hip": {
                "muzzle": ("消音器", "Suppressor"),
                "barrel": ("P90 短枪管", "P90 Short Barrel"),
                "optic": ("微型红点", "Mini Red Dot"),
                "grip": ("激光", "Laser"),
                "magazine": ("50发弹匣", "50-Round Mag"),
                "stock": ("无托", "No Stock"),
                "tip": "tip_hip"
            }
        },
        "conquest": {
            "balanced": {
                "muzzle": ("消焰器", "Flash Hider"),
                "barrel": ("P90 标准", "P90 Std"),
                "optic": ("全息", "Holographic"),
                "grip": ("斜握把", "Angled Grip"),
                "magazine": ("50发弹匣", "50-Round Mag"),
                "stock": ("折叠托", "Collapsible Stock"),
                "tip": "tip_bal"
            }
        },
        "pve": {
            "hip": {
                "muzzle": ("消音器", "Suppressor"),
                "barrel": ("P90 短管", "P90 Short"),
                "optic": ("红点", "Red Dot"),
                "grip": ("激光", "Laser"),
                "magazine": ("50发弹匣", "50-Round Mag"),
                "stock": ("轻型托", "Lightweight Stock"),
                "tip": "tip_hip"
            }
        }
    },
    "mini14": {
        "large": {
            "far": {
                "muzzle": ("制退器", "Compensator"),
                "barrel": ("Mini14 长枪管", "Mini14 Long Barrel"),
                "optic": ("6倍镜", "6x Scope"),
                "grip": ("垂直握把", "Vertical Grip"),
                "magazine": ("20发扩容", "20-Round Mag"),
                "stock": ("固定托", "Fixed Stock"),
                "tip": "tip_far"
            }
        },
        "close": {},
        "conquest": {
            "balanced": {
                "muzzle": ("消焰器", "Flash Hider"),
                "barrel": ("Mini14 标准", "Mini14 Std"),
                "optic": ("4倍ACOG", "4x ACOG"),
                "grip": ("直握把", "Vertical Grip"),
                "magazine": ("20发标准", "20-Round Std"),
                "stock": ("可调托", "Adjustable Stock"),
                "tip": "tip_bal"
            }
        },
        "pve": {
            "far": {
                "muzzle": ("消音器", "Suppressor"),
                "barrel": ("Mini14 长管", "Mini14 Long"),
                "optic": ("4倍镜", "4x Scope"),
                "grip": ("垂直握把", "Vertical Grip"),
                "magazine": ("20发扩容", "20-Round Mag"),
                "stock": ("战术托", "Tactical Stock"),
                "tip": "tip_far"
            }
        }
    },
    "m24": {
        "large": {
            "far": {
                "muzzle": ("消音器", "Suppressor"),
                "barrel": ("M24 重型枪管", "M24 Heavy Barrel"),
                "optic": ("8倍狙击镜", "8x Sniper Scope"),
                "grip": ("垂直握把", "Vertical Grip"),
                "magazine": ("5发扩容", "5-Round Mag"),
                "stock": ("固定托", "Fixed Stock"),
                "tip": "tip_far"
            }
        },
        "close": {},
        "conquest": {
            "far": {
                "muzzle": ("消焰器", "Flash Hider"),
                "barrel": ("M24 标准", "M24 Std"),
                "optic": ("6倍镜", "6x Scope"),
                "grip": ("战术握把", "Tactical Grip"),
                "magazine": ("5发标准", "5-Round Std"),
                "stock": ("固定托", "Fixed Stock"),
                "tip": "tip_far"
            }
        },
        "pve": {
            "far": {
                "muzzle": ("消音器", "Suppressor"),
                "barrel": ("M24 长管", "M24 Long"),
                "optic": ("8倍镜", "8x Scope"),
                "grip": ("垂直握把", "Vertical Grip"),
                "magazine": ("5发扩容", "5-Round Mag"),
                "stock": ("战术托", "Tactical Stock"),
                "tip": "tip_far"
            }
        }
    },
    "m249": {
        "large": {
            "balanced": {
                "muzzle": ("高效制退器", "High-Efficiency Compensator"),
                "barrel": ("M249 重型枪管", "M249 Heavy Barrel"),
                "optic": ("4倍ACOG", "4x ACOG"),
                "grip": ("垂直握把", "Vertical Grip"),
                "magazine": ("100发弹链", "100-Round Belt"),
                "stock": ("固定托", "Fixed Stock"),
                "tip": "tip_bal"
            }
        },
        "close": {},
        "conquest": {
            "balanced": {
                "muzzle": ("制退器", "Compensator"),
                "barrel": ("M249 标准", "M249 Std"),
                "optic": ("全息", "Holographic"),
                "grip": ("直握把", "Vertical Grip"),
                "magazine": ("100发弹链", "100-Round Belt"),
                "stock": ("可调托", "Adjustable Stock"),
                "tip": "tip_bal"
            }
        },
        "pve": {
            "balanced": {
                "muzzle": ("消焰器", "Flash Hider"),
                "barrel": ("M249 标准", "M249 Std"),
                "optic": ("2倍镜", "2x Scope"),
                "grip": ("斜握把", "Angled Grip"),
                "magazine": ("100发弹链", "100-Round Belt"),
                "stock": ("轻型托", "Lightweight Stock"),
                "tip": "tip_bal"
            }
        }
    },
    "saiga12": {
        "large": {},
        "close": {
            "hip": {
                "muzzle": ("喉缩", "Choke"),
                "barrel": ("Saiga 短枪管", "Saiga Short Barrel"),
                "optic": ("红点", "Red Dot"),
                "grip": ("战术握把", "Tactical Grip"),
                "magazine": ("8发弹匣", "8-Round Mag"),
                "stock": ("折叠托", "Collapsible Stock"),
                "tip": "tip_hip"
            }
        },
        "conquest": {
            "hip": {
                "muzzle": ("喉缩", "Choke"),
                "barrel": ("Saiga 标准", "Saiga Std"),
                "optic": ("全息", "Holographic"),
                "grip": ("垂直握把", "Vertical Grip"),
                "magazine": ("8发弹匣", "8-Round Mag"),
                "stock": ("固定托", "Fixed Stock"),
                "tip": "tip_hip"
            }
        },
        "pve": {
            "hip": {
                "muzzle": ("消音器", "Suppressor"),
                "barrel": ("Saiga 短管", "Saiga Short"),
                "optic": ("红点", "Red Dot"),
                "grip": ("激光", "Laser"),
                "magazine": ("8发弹匣", "8-Round Mag"),
                "stock": ("轻型托", "Lightweight Stock"),
                "tip": "tip_hip"
            }
        }
    },
    "glock17": {
        "large": {},
        "close": {
            "hip": {
                "muzzle": ("消音器", "Suppressor"),
                "barrel": ("Glock 短枪管", "Glock Short Barrel"),
                "optic": ("微型红点", "Mini Red Dot"),
                "grip": ("激光", "Laser"),
                "magazine": ("17发扩容", "17-Round Mag"),
                "stock": ("无", "None"),
                "tip": "tip_hip"
            }
        },
        "conquest": {},
        "pve": {
            "hip": {
                "muzzle": ("消音器", "Suppressor"),
                "barrel": ("Glock 标准", "Glock Std"),
                "optic": ("红点", "Red Dot"),
                "grip": ("激光", "Laser"),
                "magazine": ("17发扩容", "17-Round Mag"),
                "stock": ("无", "None"),
                "tip": "tip_hip"
            }
        }
    }
}

# ==============================
# 全局异常处理
# ==============================
def excepthook(exc_type, exc_value, exc_tb):
    log_path = os.path.join(os.path.dirname(sys.executable), "error.log")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("".join(traceback.format_exception(exc_type, exc_value, exc_tb)))
    QMessageBox.critical(None, "启动错误", f"程序启动失败！\n\n错误已保存至：\n{log_path}")

sys.excepthook = excepthook

# ==============================
# 主窗口类
# ==============================
class DeltaGunApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_lang = "zh"
        self.init_ui()

    def init_ui(self):
        tr = LANGUAGES[self.current_lang]
        self.setWindowTitle(tr["title"])
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()

        # 地图选择
        map_layout = QHBoxLayout()
        map_layout.addWidget(QLabel(tr["select_map"]))
        self.map_combo = QComboBox()
        self.map_combo.addItems([
            tr["map_large"], tr["map_close"],
            tr["map_conquest"], tr["map_pve"]
        ])
        self.map_combo.setCurrentIndex(0)
        map_layout.addWidget(self.map_combo)
        layout.addLayout(map_layout)

        # 枪械选择（12 把）
        gun_layout = QHBoxLayout()
        gun_layout.addWidget(QLabel(tr["select_gun"]))
        self.gun_combo = QComboBox()
        self.gun_combo.addItems([
            tr["ak47"], tr["m4a1"], tr["mp5"], tr["scar"], tr["m870"],
            tr["qbz95"], tr["p90"], tr["mini14"], tr["m24"],
            tr["m249"], tr["saiga12"], tr["glock17"]
        ])
        gun_layout.addWidget(self.gun_combo)
        layout.addLayout(gun_layout)

        # 风格选择
        self.rb_far = QRadioButton(tr["long_range"])
        self.rb_hip = QRadioButton(tr["hipfire"])
        self.rb_bal = QRadioButton(tr["balanced"])
        self.rb_bal.setChecked(True)
        layout.addWidget(self.rb_far)
        layout.addWidget(self.rb_hip)
        layout.addWidget(self.rb_bal)

        # 按钮
        btn_layout = QHBoxLayout()
        self.btn_gen = QPushButton(tr["generate"])
        self.btn_lang = QPushButton(f"🌐 {tr['lang_switch']}")
        self.btn_gen.clicked.connect(self.generate)
        self.btn_lang.clicked.connect(self.toggle_lang)
        btn_layout.addWidget(self.btn_gen)
        btn_layout.addWidget(self.btn_lang)
        layout.addLayout(btn_layout)

        # 结果
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setMaximumHeight(260)
        layout.addWidget(self.result)

        central.setLayout(layout)
        self.resize(700, 540)

    def toggle_lang(self):
        self.current_lang = "en" if self.current_lang == "zh" else "zh"
        tr = LANGUAGES[self.current_lang]
        self.setWindowTitle(tr["title"])
        
        # 更新地图
        self.map_combo.setItemText(0, tr["map_large"])
        self.map_combo.setItemText(1, tr["map_close"])
        self.map_combo.setItemText(2, tr["map_conquest"])
        self.map_combo.setItemText(3, tr["map_pve"])
        
        # 更新枪械
        guns = ["ak47", "m4a1", "mp5", "scar", "m870",
                "qbz95", "p90", "mini14", "m24",
                "m249", "saiga12", "glock17"]
        for i, key in enumerate(guns):
            self.gun_combo.setItemText(i, tr[key])
        
        # 更新风格
        self.rb_far.setText(tr["long_range"])
        self.rb_hip.setText(tr["hipfire"])
        self.rb_bal.setText(tr["balanced"])
        self.btn_gen.setText(tr["generate"])
        self.btn_lang.setText(f"🌐 {tr['lang_switch']}")

    def generate(self):
        tr = LANGUAGES[self.current_lang]
        
        map_index = self.map_combo.currentIndex()
        gun_index = self.gun_combo.currentIndex()
        map_key = MAP_KEYS[map_index]
        gun_keys = ["ak47", "m4a1", "mp5", "scar", "m870",
                   "qbz95", "p90", "mini14", "m24",
                   "m249", "saiga12", "glock17"]
        gun_key = gun_keys[gun_index]
        
        style = None
        if self.rb_far.isChecked():
            style = "far"
        elif self.rb_hip.isChecked():
            style = "hip"
        elif self.rb_bal.isChecked():
            style = "balanced"
        else:
            self.result.setPlainText(tr["select_style"])
            return

        if map_key not in GUN_CONFIGS[gun_key] or style not in GUN_CONFIGS[gun_key][map_key]:
            msg = "该地图下无此配装推荐" if self.current_lang == "zh" else "No recommendation for this map/style"
            self.result.setPlainText(f"⚠️ {msg}")
            return

        config_data = GUN_CONFIGS[gun_key][map_key][style]
        config = {}
        for key, value in config_data.items():
            if key == "tip":
                config["tip"] = tr[value]
            else:
                zh_val, en_val = value
                config[tr[key]] = zh_val if self.current_lang == "zh" else en_val

        text = f"<h3>{tr['recommended']}</h3><ul>"
        for k, v in config.items():
            if k != "tip":
                text += f"<li><b>{k}:</b> {v}</li>"
        text += f"</ul><p><b>💡 Tip:</b> {config['tip']}</p>"
        self.result.setHtml(text)

# ==============================
# 程序入口
# ==============================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeltaGunApp()
    window.show()
    sys.exit(app.exec())