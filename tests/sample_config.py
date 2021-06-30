from collections import OrderedDict

sample_config = OrderedDict(
    [
        (
            "suffixes",
            {
                "modeling": {
                    "mesh": ["MH", "MSH", "MESH"],
                    "nurbs": ["NB", "NRB", "NURB"],
                    "poly": ["PY", "PLY", "POLY"],
                    "subd": ["SD", "SUB", "SUBD"],
                    "curve": ["CR", "CRV", "CURV"],
                    "group": ["GP", "GRP", "GROP"],
                    "locator": ["LT", "LOC", "LOCT"],
                },
                "rigging": {
                    "control": ["CT", "CTR", "CTRL"],
                    "connection_group": ["CG", "CGP", "CGRP"],
                    "offset_group": ["OG", "OGP", "OGRP"],
                    "joint": ["JT", "JNT", "JINT"],
                    "iomesh": ["IM", "IOM", "IOMH"],
                    "influence": ["IF", "INF", "INFL"],
                    "blend": ["BP", "BSP", "BSHP"],
                    "blendshape": ["BD", "BLD", "BLND"],
                    "duplicate": ["DP", "DUP", "DUPL"],
                    "follicle": ["FL", "FOL", "FOLL"],
                    "reference": ["RF", "REF", "REFR"],
                    "cluster": ["CL", "CLS", "CLTR"],
                    "point_on_curve": ["PC", "POC", "POCV"],
                    "point_on_curve_info": ["PO", "POI", "POCI"],
                    "closest_point_on_curve": ["CP", "CPC", "CPOV"],
                    "closest_point_on_curve_info": ["CI", "CPI", "CPOI"],
                    "link": ["LK", "LNK", "LINK"],
                    "unknown": ["UN", "UNK", "UNKN"],
                },
                "utility": {
                    "plusMinusAverage": ["PM", "PMA", "PMAV"],
                    "multiplyDivide": ["ML", "MUL", "MULD"],
                    "condition": ["CD", "CON", "COND"],
                    "ramp": ["RM", "RMP", "RAMP"],
                    "setRange": ["ST", "SET", "SETR"],
                },
                "dynamics": {"hairSystem": ["HS", "HRS", "HSYS"], "nucleus": ["NC", "NUC", "NUCL"]},
                "texturing": {
                    "color": ["CL", "COL", "COLR"],
                    "bump": ["BM", "BMP", "BUMP"],
                    "displacement": ["DS", "DSP", "DISP"],
                    "id": ["I", "ID", "IDS"],
                    "emissive": ["EM", "EMS", "EMIS"],
                    "opacity": ["OP", "OPC", "OPAC"],
                    "specular": ["SP", "SPC", "SPEC"],
                    "reflection": ["RF", "RFL", "REFL"],
                    "normal": ["NM", "NRM", "NRML"],
                    "transparency": ["TR", "TRY", "TRSP"],
                },
            },
        ),
        (
            "overall_config",
            {
                "version_padding": 3,
                "type_len": 3,
                "location_len": 2,
                "anatomy_len": 3,
                "discipline_len": 4,
                "purpose_len": 4,
                "height_len": 1,
                "depth_len": 1,
                "side_len": 1,
                "date_format": "%Y-%m-%d",
                "var_format": "upper",
            },
        ),
        (
            "options",
            {
                "discipline": {
                    "animation": ["AN", "ANI", "ANIM", "ANIMN"],
                    "lighting": ["LT", "LGT", "LGHT", "LIGHT"],
                    "rigging": ["RG", "RIG", "RIGG", "RIGNG"],
                    "matchmove": ["MM", "MMV", "MMOV", "MMOVE"],
                    "compositing": ["CM", "CMP", "COMP", "COMPG"],
                    "modeling": ["MD", "MOD", "MODL", "MODEL"],
                },
                "side": {
                    "left": ["l", "lf", "lft", "left"],
                    "right": ["r", "rt", "rgt", "rght"],
                    "center": ["c", "cn", "ctr", "cntr"],
                },
                "purpose": {
                    "hierarchy": ["h", "hr", "hrc", "hchy", "hrchy"],
                    "transform": ["t", "ts", "srt", "tnfm", "trans"],
                    "buffer": ["b", "bf", "buf", "buff", "buffr", "strBuffer"],
                    "component": ["c", "cm", "cmp", "cmpt", "cmpnt"],
                },
                "depth": {
                    "rear": ["r", "rr", "rea", "rear"],
                    "front": ["f", "fr", "frt", "frnt"],
                    "back": ["b", "bk", "bak", "back"],
                },
                "height": {
                    "top": ["t", "tp", "top", "topp"],
                    "bottom": ["b", "bt", "bot", "bott"],
                    "middle": ["m", "md", "mid", "midd"],
                },
                "type": {
                    "modeling": {
                        "mesh": ["MH", "MSH", "MESH"],
                        "nurbs": ["NB", "NRB", "NURB"],
                        "poly": ["PY", "PLY", "POLY"],
                        "subd": ["SD", "SUB", "SUBD"],
                        "curve": ["CR", "CRV", "CURV"],
                        "group": ["GP", "GRP", "GROP"],
                        "locator": ["LT", "LOC", "LOCT"],
                    },
                    "rigging": {
                        "control": ["CT", "CTR", "CTRL"],
                        "connection_group": ["CG", "CGP", "CGRP"],
                        "offset_group": ["OG", "OGP", "OGRP"],
                        "joint": ["JT", "JNT", "JINT"],
                        "iomesh": ["IM", "IOM", "IOMH"],
                        "influence": ["IF", "INF", "INFL"],
                        "blend": ["BP", "BSP", "BSHP"],
                        "blendshape": ["BD", "BLD", "BLND"],
                        "duplicate": ["DP", "DUP", "DUPL"],
                        "follicle": ["FL", "FOL", "FOLL"],
                        "reference": ["RF", "REF", "REFR"],
                        "cluster": ["CL", "CLS", "CLTR"],
                        "point_on_curve": ["PC", "POC", "POCV"],
                        "point_on_curve_info": ["PO", "POI", "POCI"],
                        "closest_point_on_curve": ["CP", "CPC", "CPOV"],
                        "closest_point_on_curve_info": ["CI", "CPI", "CPOI"],
                        "link": ["LK", "LNK", "LINK"],
                        "unknown": ["UN", "UNK", "UNKN"],
                    },
                    "utility": {
                        "plusMinusAverage": ["PM", "PMA", "PMAV"],
                        "multiplyDivide": ["ML", "MUL", "MULD"],
                        "condition": ["CD", "CON", "COND"],
                        "ramp": ["RM", "RMP", "RAMP"],
                        "setRange": ["ST", "SET", "SETR"],
                    },
                    "dynamics": {
                        "hairSystem": ["HS", "HRS", "HSYS"],
                        "nucleus": ["NC", "NUC", "NUCL"],
                    },
                    "texturing": {
                        "color": ["CL", "COL", "COLR"],
                        "bump": ["BM", "BMP", "BUMP"],
                        "displacement": ["DS", "DSP", "DISP"],
                        "id": ["I", "ID", "IDS"],
                        "emissive": ["EM", "EMS", "EMIS"],
                        "opacity": ["OP", "OPC", "OPAC"],
                        "specular": ["SP", "SPC", "SPEC"],
                        "reflection": ["RF", "RFL", "REFL"],
                        "normal": ["NM", "NRM", "NRML"],
                        "transparency": ["TR", "TRY", "TRSP"],
                    },
                },
                "location": {
                    "top": ["t", "tp", "top", "topp"],
                    "bottom": ["b", "bt", "bot", "bott"],
                    "middle": ["m", "md", "mid", "midd"],
                    "rear": ["r", "rr", "rea", "rear"],
                    "front": ["f", "fr", "frt", "frnt"],
                    "back": ["b", "bk", "bak", "back"],
                },
                "anatomy": {
                    "superior": ["sup", "supe"],
                    "anterior": ["ant", "ante"],
                    "medial": ["med", "medi"],
                    "lateral": ["lat", "latr"],
                    "posterior": ["pos", "post"],
                    "proximal": ["pro", "prox"],
                    "distal": ["dst", "dist"],
                    "central": ["cnt", "cent"],
                    "peripheral": ["phl", "peri"],
                    "superficial": ["sfl", "supf"],
                    "deep": ["dep", "deep"],
                    "dorsal": ["dor", "dors"],
                    "ventral": ["ven", "vent"],
                    "cranial": ["cra", "cran"],
                    "caudal": ["cau", "caud"],
                },
                "compoutput": {
                    "lighting_slap_comp": "LSC",
                    "input_graded": "IG",
                    "input": "I",
                    "asset_slap_comp": "ASC",
                    "roto": "R",
                },
                "status": {
                    "preproduction": "PREPROD",
                    "storyboard": "STORYB",
                    "initial": "INITIAL",
                    "work_in_progress": "WIP",
                    "final": "FINAL",
                    "deliverable": "DELIVER",
                },
            },
        ),
        (
            "naming_formats",
            {
                "node": {
                    "default": "side_location_nameDecoratorVar_childtype_purpose_type",
                    "format_archive": "side_name_space_purpose_decorator_childtype_type",
                },
                "texturing": {"shader": "side_name_type"},
                "riggers": {
                    "mpc": "side_location_nameDecoratorVar1(v)Var2_childtype_purpose_type",
                    "lee_wolland": "type_childtype_space_purpose_name_side",
                    "raffaele_fragapane": "name_heightSideDepth_purpose",
                },
                "rigging": {
                    "top_group": "nameDecorator_lodVar_type",
                    "joint": "side_location_nameDecoratorVar_childtype_purpose_type",
                },
                "modeling": {"top_group": "side_location_nameDecorator_lodVar_type"},
                "working_files": {
                    "asset_folder": "discipline_name_lodDecoratorVar",
                    "asset_file": "name_lodDecoratorVar_version.ext",
                    "working_file": "name_discipline_lodDecoratorVar_version_initials.ext",
                    "techops_file": "compoutput_shot_version_name_type_status_version1_date-quality_filetype.ext",
                },
            },
        ),
    ]
)
