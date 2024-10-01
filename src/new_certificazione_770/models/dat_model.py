# -*- coding: utf-8 -*-
"""
DAT CSV module

@File: dat_model.py
@Date: 2024-08-08
"""

# Built-in/Generic Imports
import csv
import datetime
import locale
import os

# Libs
from pydantic import BaseModel, Field


class DATCSVModel(BaseModel):
    """DATCSV Model Class for DAT record"""

    codice_fiscale_percipiente: str = Field(
        default="", serialization_alias="Codice fiscale percipiente"
    )
    cognome_o_denominazione: str = Field(
        default="", serialization_alias="Cognome o Denominazione"
    )
    nome: str = Field(default="", serialization_alias="Nome")
    sesso_m_f: str = Field(default="", serialization_alias="Sesso M/F")
    data_di_nascita_gg_mm_aaaa: str = Field(
        default="", serialization_alias="Data di nascita GG/MM/AAAA"
    )
    comune_di_nascita: str = Field(default="", serialization_alias="Comune di nascita")
    provincia_di_nascita: str = Field(
        default="", serialization_alias="Provincia di nascita"
    )
    categorie_particolari: str = Field(
        default="", serialization_alias="Categorie Particolari"
    )
    eventi_eccezionali: str = Field(
        default="", serialization_alias="Eventi Eccezionali"
    )
    casi_di_esclusione_dalla_precompilata: str = Field(
        default="", serialization_alias="Casi di esclusione dalla precompilata"
    )
    stato_estero: str = Field(default="", serialization_alias="Stato Estero")
    comune_domicilio_al_1_1_2023: str = Field(
        default="", serialization_alias="Comune domicilio al 1/1/2023"
    )
    provincia_domicilio_al_1_1_2023: str = Field(
        default="", serialization_alias="Provincia domicilio al 1/1/2023"
    )
    codice_comune_domicilio_al_1_1_2023: str = Field(
        default="", serialization_alias="Codice comune domicilio al 1/1/2023"
    )
    fusione_comuni_al_1_1_23: str = Field(
        default="", serialization_alias="Fusione Comuni al 1/1/23"
    )
    comune_domicilio_al_1_1_2024: str = Field(
        default="", serialization_alias="Comune domicilio al 1/1/2024"
    )
    provincia_domicilio_al_1_1_2024: str = Field(
        default="", serialization_alias="Provincia domicilio al 1/1/2024"
    )
    codice_comune_domicilio_al_1_1_2024: str = Field(
        default="", serialization_alias="Codice comune domicilio al 1/1/2024"
    )
    fusione_comuni_al_1_1_2024: str = Field(
        default="", serialization_alias="Fusione Comuni al 1/1/2024"
    )
    dati_relativi_al_rappresentante_codice_fiscale_rappresentante_: str = Field(
        default="",
        serialization_alias="Dati relativi al rappresentante - Codice fiscale Rappresentante",
    )
    indirizzo_di_residenza_sede_legale_o_se_diverso_domicilio_fiscale_comune: str = Field(
        default="",
        serialization_alias="Indirizzo di residenza/Sede legale o (se diverso) Domicilio Fiscale - Comune",
    )
    indirizzo_di_residenza_sede_legale_o_se_diverso_domicilio_fiscale_provincia_sigla: str = Field(
        default="",
        serialization_alias="Indirizzo di residenza/Sede legale o (se diverso) Domicilio Fiscale - Provincia (sigla)",
    )
    indirizzo_di_residenza_sede_legale_o_se_diverso_domicilio_fiscale_frazione_via_e_numero_civico: str = Field(
        default="",
        serialization_alias="Indirizzo di residenza/Sede legale o (se diverso) Domicilio Fiscale - Frazione, via e numero civico",
    )
    indirizzo_di_residenza_sede_legale_o_se_diverso_domicilio_fiscale_cap: str = Field(
        default="",
        serialization_alias="Indirizzo di residenza/Sede legale o (se diverso) Domicilio Fiscale - C.a.p.",
    )
    indirizzo_di_residenza_sede_legale_o_se_diverso_domicilio_fiscale_posta_elettronica: str = Field(
        default="",
        serialization_alias="Indirizzo di residenza/Sede legale o (se diverso) Domicilio Fiscale - Posta Elettronica",
    )
    codice_di_identificazione_fiscale_estero: str = Field(
        default="", serialization_alias="Codice di identificazione fiscale estero"
    )
    localita_residenza_estera: str = Field(
        default="", serialization_alias="Località residenza estera"
    )
    via_e_numero_civico: str = Field(
        default="", serialization_alias="Via e numero civico"
    )
    non_residenti_shumacker: str = Field(
        default="", serialization_alias="Non Residenti Shumacker"
    )
    codice_stato_estero: str = Field(
        default="", serialization_alias="Codice Stato Estero"
    )
    causale: str = Field(default="", serialization_alias="Causale")
    anno: str = Field(default="", serialization_alias="Anno")
    anticipazione: str = Field(default="", serialization_alias="Anticipazione")
    ammontare_lordo_corrisposto: str = Field(
        default="", serialization_alias="Ammontare lordo corrisposto"
    )
    somme_non_soggette_a_ritenuta_per_regime_convenzionale: str = Field(
        default="",
        serialization_alias="Somme non soggette a ritenuta per regime convenzionale",
    )
    codice_altre_somme_non_soggette: str = Field(
        default="", serialization_alias="Codice altre somme non soggette"
    )
    altre_somme_non_soggette_a_ritenuta: str = Field(
        default="", serialization_alias="Altre somme non soggette a ritenuta"
    )
    ritenute_a_titolo_di_acconto: str = Field(
        default="", serialization_alias="Ritenute a titolo di acconto"
    )
    ritenute_a_titolo_di_imposta: str = Field(
        default="", serialization_alias="Ritenute a titolo di imposta"
    )
    ritenute_sospese: str = Field(default="", serialization_alias="Ritenute sospese")
    addizionale_regionale_a_titolo_d_acconto: str = Field(
        default="", serialization_alias="Addizionale regionale a titolo di acconto"
    )
    addizionale_regionale_a_titolo_dimposta: str = Field(
        default="", serialization_alias="Addizionale regionale a titolo di imposta"
    )
    addizionale_regionale_sospesa: str = Field(
        default="", serialization_alias="Addizionale regionale sospesa"
    )
    addizionale_comunale_a_titolo_dacconto: str = Field(
        default="", serialization_alias="Addizionale comunale a titolo di acconto"
    )
    addizionale_comunale_a_titolo_dimposta: str = Field(
        default="", serialization_alias="Addizionale comunale a titolo di imposta"
    )
    addizionale_comunale_sospesa: str = Field(
        default="", serialization_alias="Addizionale comunale sospesa"
    )
    imponibile_anni_precedenti: str = Field(
        default="", serialization_alias="Imponibile anni precedenti"
    )
    ritenute_operate_anni_precedenti: str = Field(
        default="", serialization_alias="Ritenute operate anni precedenti"
    )
    spese_rimborsate: str = Field(default="", serialization_alias="Spese rimborsate")
    ritenute_rimborsate: str = Field(
        default="", serialization_alias="Ritenute rimborsate"
    )
    somme_restituite_al_netto_della_ritenuta_subita: str = Field(
        default="",
        serialization_alias="Somme restituite al netto della ritenuta subita",
    )
    codice_fiscale_ente_previdenziale: str = Field(
        default="", serialization_alias="Codice Fiscale Ente Previdenziale"
    )
    denominazione_ente_previdenziale: str = Field(
        default="", serialization_alias="Denominazione Ente previdenziale"
    )
    codice_azienda: str = Field(default="", serialization_alias="Codice Azienda")
    categoria: str = Field(default="", serialization_alias="Categoria")
    contributi_previdenziali_a_carico_del_soggetto_erogante: str = Field(
        default="",
        serialization_alias="Contributi Previdenziali a carico del soggetto erogante",
    )
    contributi_previdenziali_a_carico_del_percipiente: str = Field(
        default="",
        serialization_alias="Contributi previdenziali a carico del percipiente",
    )
    altri_contributi: str = Field(default="", serialization_alias="Altri contributi")
    importo_altri_contributi: str = Field(
        default="", serialization_alias="Importo altri contributi"
    )
    contributi_dovuti: str = Field(default="", serialization_alias="Contributi dovuti")
    contributi_versati: str = Field(
        default="", serialization_alias="Contributi versati"
    )
    somme_corrisposte_prima_della_data_del_fallimento: str = Field(
        default="",
        serialization_alias="Somme corrisposte prima della data del fallimento",
    )
    somme_corrisposte_dal_curatore_commissario: str = Field(
        default="", serialization_alias="Somme corrisposte dal curatore/ commissario"
    )
    sez_altri_soggetti_codice_fiscale: str = Field(
        default="", serialization_alias="Sez. Altri soggetti - Codice Fiscale"
    )
    sez_altri_soggetti_imponibile: str = Field(
        default="", serialization_alias="Sez. Altri soggetti - Imponibile"
    )
    sez_altri_soggetti_ritenute_a_titolo_di_acconto: str = Field(
        default="",
        serialization_alias="Sez. Altri soggetti - Ritenute a titolo di acconto",
    )
    sez_altri_soggetti_ritenute_a_titolo_dimposta: str = Field(
        default="",
        serialization_alias="Sez. Altri soggetti - Ritenute a titolo di imposta",
    )
    sez_altri_soggetti_ritenute_sospese: str = Field(
        default="", serialization_alias="Sez. Altri soggetti - Ritenute sospese"
    )
    sez_altri_soggetti_addizionale_regionale_a_titolo_di_acconto: str = Field(
        default="",
        serialization_alias="Sez. Altri soggetti - Addizionale regionale a titolo di acconto",
    )
    sez_altri_soggetti_addizionale_regionale_a_titolo_dimposta: str = Field(
        default="",
        serialization_alias="Sez. Altri Soggetti - Addizionale regionale a titolo di imposta",
    )
    sez_altri_soggetti_addizionale_regionale_sospesa: str = Field(
        default="",
        serialization_alias="Sez. Altri Soggetti - Addizionale regionale sospesa",
    )
    sez_altri_soggetti_addizionale_comunale_a_titolo_dacconto: str = Field(
        default="",
        serialization_alias="Sez. Altri soggetti - Addizionale comunale a titolo di acconto",
    )
    sez_altri_soggetti_addizionale_comunale_a_titolo_dimposta: str = Field(
        default="",
        serialization_alias="Sez. Altri soggetti - Addizionale comunale a titolo di imposta",
    )
    sez_altri_soggetti_addizionale_comunale_sospesa: str = Field(
        default="",
        serialization_alias="Sez. Altri soggetti - Addizionale comunale sospesa",
    )
    casi_particolari_operazioni_straordinarie_codice_fiscale_sezione_lavoro_autonomo_e_redditi_diversi: str = Field(
        default="",
        serialization_alias="Casi particolari operazioni straordinarie - Codice fiscale sezione lavoro autonomo e redditi diversi",
    )
    data_firma_sostituto_dimposta: str = Field(
        default="", serialization_alias="Data firma sostituto di imposta"
    )


# Constants
DAT_FILE_PRENAME = "DAT-EXPORT"
DAT_FILE_POSTNAME = "v3.0"
DAT_FILE_EXT = "csv"
DAT_CSV_DELIMITER = ";"


class DATFile:
    """DATFile class for manage CSV DAT file"""

    def __init__(
        self,
        path: str,
        code_ente_prev: str,
        denom_ente_prev: str,
        code_somme_non_sogg: str,
        data_firma: str,
    ):
        # Input fields
        self.path: str = path
        self.code_ente_prev: str = code_ente_prev
        self.denom_ente_prev: str = denom_ente_prev
        self.code_somme_non_sogg: str = code_somme_non_sogg
        self.data_firma: str = data_firma

        # Internal fields
        self._csv_fname: str | None = None
        self._csv_fd = None
        self._csv_writer = None
        self._headers = None

    @property
    def headers(self) -> list[str | None]:
        if self._headers is None:
            headers = [v.serialization_alias for v in DATCSVModel.model_fields.values()]
            self._headers = headers
        return self._headers

    @property
    def file_name(self) -> str:
        if self._csv_fname is None:
            dt = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{DAT_FILE_PRENAME}-{dt}-{DAT_FILE_POSTNAME}.{DAT_FILE_EXT}"
            self._csv_fname = os.path.join(self.path, file_name)
        return self._csv_fname

    def _set_headers(self):
        """Set CSV header fields"""
        headers = [v.serialization_alias for v in DATCSVModel.model_fields.values()]
        self._headers = headers

    def _start_CSV(self):
        """Create a CSV file if none exists."""
        if self._csv_fd:
            self._csv_fd.close()
        self._csv_fd = open(file=self.file_name, mode="at", encoding="utf-8")
        self._csv_writer = csv.writer(
            self._csv_fd,
            delimiter=";",
            quoting=csv.QUOTE_MINIMAL,
            skipinitialspace=True,
            lineterminator="\n",
        )
        self._csv_writer.writerow(self.headers)
        self._csv_fd.flush()

    def start(self):
        """Start class instance"""
        self._start_CSV()

    @staticmethod
    def _format_float(value) -> str:
        """(static) Format float string with comma."""
        val = float(value)
        locale.setlocale(category=locale.LC_ALL, locale="it_IT.UTF-8")
        text: str = f"{val:z.2f}".replace(".", ",")
        return text

    def _transform_data_into_datcsv(self, record: list) -> DATCSVModel:
        """(Static) Trasform a list of values in DATCSVModel"""
        try:
            rec_json = {
                "codice_fiscale_percipiente": str(record[0]).upper(),
                "cognome_o_denominazione": str(record[1]).upper(),
                "nome": str(record[2]).upper(),
                "sesso_m_f": str(record[3]).upper(),
                "data_di_nascita_gg_mm_aaaa": (record[4]).strftime(r"%d/%m/%Y"),
                "comune_di_nascita": str(record[5]).upper(),
                "provincia_di_nascita": str(record[6]).upper(),
                "causale": "V",
                # somme
                "ammontare_lordo_corrisposto": DATFile._format_float(record[7]),
                "codice_altre_somme_non_soggette": self.code_somme_non_sogg,
                "altre_somme_non_soggette_a_ritenuta": DATFile._format_float(record[8]),
                "ritenute_a_titolo_di_imposta": DATFile._format_float(record[9]),
            }
            if float(record[10]) > float(0):
                rec_extra = {
                    "codice_fiscale_ente_previdenziale": self.code_ente_prev,
                    "denominazione_ente_previdenziale": self.denom_ente_prev,
                    "contributi_previdenziali_a_carico_del_soggetto_erogante": DATFile._format_float(
                        # ! BUGFIX: wrong amount bug
                        float(record[10]) * 2
                    ),
                    "contributi_previdenziali_a_carico_del_percipiente": DATFile._format_float(
                        record[10]
                    ),
                    "contributi_dovuti": DATFile._format_float(float(record[10]) * 3),
                    "contributi_versati": DATFile._format_float(float(record[10]) * 3),
                }
                rec_json.update(rec_extra)

            rec_json.update(
                {
                    "data_firma_sostituto_dimposta": datetime.date.fromisoformat(
                        self.data_firma
                    ).strftime(r"%d/%m/%Y"),
                }
            )
            rec = DATCSVModel.model_validate(rec_json)
            return rec
        except Exception as e:
            raise e

    def write_record(self, data):
        """Write record in CSV DAT file."""
        record = self._transform_data_into_datcsv(record=data)
        row_dict = record.model_dump(by_alias=True)
        if self._csv_writer is None:
            self._start_CSV()
        self._csv_writer.writerow(row_dict.values())
        self._csv_fd.flush()

    def __exit__(self):
        if self._csv_fd and not self._csv_fd.closed:
            self._csv_fd.close()
            self._csv_writer = None
