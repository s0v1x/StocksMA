from types import MappingProxyType

import pytest

from StocksMA.constants import COMPANIES, CompanyInfo
from StocksMA import get_isin
from StocksMA.exceptions import CompanyNotFoundException


class TestCompaniesConst:
    def test_company_info_struct(self):
        assert CompanyInfo._fields == ("name", "other_name", "isin")

    def test_companies_const_type(self):
        assert isinstance(COMPANIES,  MappingProxyType)

    def test_read_only_access_to_companies_const(self):
        with pytest.raises(TypeError):
            COMPANIES["StocksMA"] = CompanyInfo("X", "Y", "Z")

    @pytest.mark.parametrize("ticker", COMPANIES.keys())
    def test_companies_const_keys_type(self, ticker):
        assert isinstance(ticker,  str)

    @pytest.mark.parametrize("company_info", COMPANIES.values())
    def test_companies_const_values_type(self, company_info):
        assert isinstance(company_info, CompanyInfo)

    @pytest.mark.parametrize("company_info", COMPANIES.values())
    def test_companies_info_values_type(self, company_info):
        assert isinstance(company_info.name, str)
        assert isinstance(company_info.other_name, str)
        assert isinstance(company_info.isin, str)

    def test_isin_uniqueness(self):
        isins = [info.isin for info in COMPANIES.values()]
        assert len(set(isins)) == len(isins)

    @pytest.mark.parametrize(
        "isin", [info.isin for info in COMPANIES.values()]
    )
    def test_isin_validity(self, isin):
        assert len(isin) == 12
        assert isin.startswith("MA")
        assert isin[2:].isdigit()

    def test_company_name_uniqueness(self):
        names = [info.name for info in COMPANIES.values()]
        assert len(set(names)) == len(names)

    def test_other_name_uniqueness(self):
        other_names = [info.other_name for info in COMPANIES.values()]
        assert len(set(other_names)) == len(other_names)

class TestGetISIN:
    @pytest.mark.parametrize("company", [10, 12.2, object])
    def test_get_isin_iputs_validity(self, company):
        with pytest.raises(ValueError):
            get_isin(company)


    @pytest.mark.parametrize("company", ["StocksMA", "AAA", "_BAM"])
    def test_get_isin_company_not_found_excp(self, company):
        with pytest.raises(CompanyNotFoundException):
            get_isin(company)

    @pytest.mark.parametrize(
        ["company", "expected_isin"],
        [(info.name, info.isin) for info in COMPANIES.values()]
        )
    def test_isin_on_all_availble_company_names(self, company, expected_isin):
        name, isin = get_isin(company)

        assert name.upper() == company.upper()
        assert isin == expected_isin


    @pytest.mark.parametrize(
        ["ticker", "expected_isin"],
        [(ticker, info.isin) for ticker, info in COMPANIES.items()]
        )
    def test_isin_on_all_availble_tickers(self, ticker, expected_isin):
        _, isin = get_isin(ticker)

        assert isin == expected_isin
