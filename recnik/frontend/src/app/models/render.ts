export interface TipRendera {
    id: number;
    naziv: string;
}

export interface Render {
    id: number;
    vreme_rendera: Date;
    opis: string;
    napomena: string;
    tip_dokumenta: TipRendera;
    rendered_file: string;
}
